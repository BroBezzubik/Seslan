$(document).ready(function(){
  let width = $('#game-container').width();
  let height = $('#game-container').height();
  let container_id = '#game-container'
  let game = new Game(container_id, width, height)
  game.Map.initMap();
  game.Map.initMapScaling();
  game.Map.initContextMenu();
  game.updateEvents();
  game.loop();
});


class Player{

  constructor(login="Login", profession="proffesion", description='some description'){
    this.login = login
    this.profession = profession
    this.description = description
    this.loaded_news = []
  }

}


class GameMap{

  constructor(container_id = '#game-container' , width, height){
    this.stage = new Konva.Stage({
      container: container_id,
      width:width,
      height:height,
      draggable:true,
    })
    this.scale = 1.1;
    this.layer_map = new Konva.Layer();
    this.layer_events = new Konva.Layer();
    this.stage.add(this.layer_map);
    this.stage.add(this.layer_events);
  }

  loadMapImage(layer) {
    return new Promise( (resolve, reject) =>{
      let map = new Image();
      fetch('ajax_get_game_map')
      .then(response => response.json())
      .then(data => {
        map.src = data['map_url']
      })
      map.onload = function(){
        let img = new Konva.Image({
            Image: map,
        })
        
        resolve(img)
      }
      
    })

  }

  initMap() {

    this.loadMapImage(this.layer_map)
    .then( image =>{ this.layer_map.add(image); this.layer_map.draw()});

  }

  initMapScaling(){
    let scaleBy = 1.1;
    this.stage.on('wheel', (e) => {
      e.evt.preventDefault();
      var oldScale = this.stage.scaleX();

      var pointer = this.stage.getPointerPosition();

      var mousePointTo = {
        x: (pointer.x - this.stage.x()) / oldScale,
        y: (pointer.y - this.stage.y()) / oldScale,
      };

      var newScale =
        e.evt.deltaY > 0 ? oldScale * scaleBy : oldScale / scaleBy;

        this.stage.scale({ x: newScale, y: newScale });

      var newPos = {
        x: pointer.x - mousePointTo.x * newScale,
        y: pointer.y - mousePointTo.y * newScale,
      };
      this.stage.position(newPos);
      this.stage.draw();
    });
  }

  initContextMenu(){
    let layer_events = this.layer_events;
    let stage = this.stage
    
    let currentEvent = null;
    let $menu = $('#context-menu');
    $('#context-menu-infomation').bind("click", () => {});

    document.body.onkeyup = (e) => {
      if (e.keyCode == 32){
        let pos = this.getRelativePointerPosition(this.layer_map);
        alert( [Math.floor(pos.x), Math.floor(pos.y)] )
      }
    }
     
    
    $('#context-menu-moveTo').bind("click", () => alert("Move to"));

    $(window).click(() =>{
      $menu.css('display', 'none');
    })
    
    this.stage.on('contextmenu', (e) => {
      e.evt.preventDefault()
    })

    this.layer_events.on('contextmenu', function(e){
      e.evt.preventDefault();
      if (e.target === layer_events){
        return;
      }

      let currentEvent = e.target;
      
      let containerRect = stage.container().getBoundingClientRect();
      $menu.css('display', 'initial');
      $menu.css('top', containerRect.top + stage.getPointerPosition().y + 4 + 'px');
      $menu.css('left', containerRect.left + stage.getPointerPosition().y + 4 + 'px');
      fetch('ajax_get_url_info_event_' + currentEvent.id().split('_')[1])
      .then(response => response.json())
      .then(data => {
        $('#information-url').attr('href', data["url"]);
        $('#context-menu-event-name').text(data["event_name"]);
      })
    })
  }

  getRelativePointerPosition(node){
    let transform = node.getAbsoluteTransform().copy();
    transform.invert();
    let pos = node.getStage().getPointerPosition();
    return transform.point(pos)
  }
}

  
class Game {

  constructor (container_id, width, height){
    this.Map = new GameMap(container_id, width, height)
    this.Player = new Player();
  }

  loop(){
    let self = this;
    setInterval( () => self.updateEvents(), 3000);
  }

  public_news(event_name, data){
    let text = '';
    
    if (data['is_news'] == true & !this.Player.loaded_news.includes(event_name)){
      $('#news-list').append("<li class='list-group-item'><div class='news-card'>" + 
      "<img src='" + data['url'] + "'" + " align='right'><p>" + text.concat('\n', data['descriptions']) + "</p></div></li>");
      this.Player.loaded_news.push(event_name)
    }
    
  }

  getCookie(name) {

    if (!document.cookie) {
      return null;
    }

    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));
    if (xsrfCookies.length === 0) {
      return null;
    }
    
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);

  }

  updateEvents(layer = this.layer_events){
    layer = this.Map.layer_events
    /* получаем список событий загруженных игроку */
    let js_data = { };
  
    
    /* Полученте csrt token */
    let csrtfToken = this.getCookie('csrftoken');
  
    /*запрос событий*/
    fetch('ajax_update_events', {
      method: "POST",
      credentials: "same-origin",
      body: JSON.stringify(js_data),
      headers : {
        'Content-Type' : 'application/json',
        "Accept": "application/json",
        "X-XSRF-TOKEN" : csrtfToken,
      }
    })
    .then(response => response.json())
    .then( data => {
      for (event in data){
        this.load_events(layer, event, data[event]);
        this.public_news(event, data[event]);
      }
      
    })
    layer.draw();
  }

  load_events(layer = this.layer_events, event_name, event_data){
    return new Promise( (resolve, reject) =>{
      let event = layer.findOne('#' + event_name);
      if (event === undefined){
        let event_image = new Image();
        event_image.src = event_data['url'];
        event_image.onload = function(){
          let img = new Konva.Image({
            id: event_name,
            name: 'event',
            x: event_data['x'],
            y: event_data['y'],
            Image: event_image,
        })
          img.on('mouseover', () =>{
            layer.getParent().container().style.cursor = 'pointer';
          })
  
          img.on('mouseleave', () =>{
            layer.getParent().container().style.cursor = 'default';
          })
          img.cache();
          img.drawHitFromCache();
          layer.add(img);
        }
      } else {
        event.x(event_data['x']);
        event.y(event_data['y']);
      }
        resolve(layer)
    })
  }

  

}
