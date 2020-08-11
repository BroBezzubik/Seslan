from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse, Http404
from django.urls import reverse
import json


from . import models

# Create your views here.

def index(request):
    return render(request, "game/base_seslan.html")


def select_game(request):
    return HttpResponse("OK")


def game(request, game_id):
    if request.user.is_authenticated:
        content = {}
        content['UserName'] = request.user.username
        content['Moderator'] = request.user.is_superuser
        content['timeFlow'] = reverse('admin:game_game_change', args=(game_id,))
        content['addEventUrl'] = reverse('admin:game_game_event_add')
        content['addDescriptionUrl'] = reverse('admin:game_description_add')
        responce = render(request, "game/base_game.html", content)
        responce.set_cookie(key="game_id", value=game_id,)
        return responce
    else:
        return redirect("login")


def event_info(request, event_id):
    if request.method == 'GET' and request.user.is_authenticated:

        game_id = request.COOKIES['game_id']
        player = models.Player.objects.get(user_id=request.user.id)
        event = models.Game_event.objects.get(pk = event_id)
        descriptions = models.Description.objects.filter(player_id = player.id).filter(event__game = game_id).filter(event = event)
        print(descriptions)
        
        if not descriptions:
            raise Http404("Вам недоступна данная информация")
        
        descriptions_array = []
        for description in descriptions:
            description_text = "{}: {}".format(description.information.name, description.information.text)
            descriptions_array.append(description_text)

        event_description = descriptions_array
        url = event.image.file_field.url

        return render(request, "game/base_event_info.html", {"image_url": url, "event_description" : event_description})
    else:  
        raise Http404("Что то пошло не так")


def ajax_get_url_event_info(request, event_id):
    if request.method == 'GET':
        return JsonResponse({'url' : '/game/event_info/' + str(event_id), 'event_name': models.Game_event.objects.get(id=event_id).name})


def ajax_get_game_map(request):
    if request.method == 'GET':
        game = models.Game.objects.get(id=request.COOKIES['game_id'])
        map_name = game.map.name
        response = JsonResponse({"map_url" : "/media/Maps/" + map_name,})
        response.status_code = 200
        return response


def ajax_update_events(request):
    if request.method == 'POST' and request.user.is_authenticated:
        
        game_id = request.COOKIES['game_id']
        player = models.Player.objects.get(user_id=request.user.id)
        game_events = models.Game_event.objects.filter(game_id = game_id)
        descriptions = models.Description.objects.filter(player_id = player.id, event__game = game_id)
        game_time = models.Game.objects.get(id = request.COOKIES['game_id']).game_time
        
        response_json = {}

        for event in game_events:

            # Проверка свершения событий
            if game_time < event.time:
                continue

            event_descriptions = descriptions.filter(event = event)
            event_json = {}
            json_event_name = 'event_'+ str(event.id)
            event_image = event.image
            url = event_image.file_field.url
            x = event.pos_x
            y = event.pos_y
            
            descriptions_text = []

            for description in event_descriptions:
                description = '{}: {}\n'.format(description.information.name, (description.information.text))
                descriptions_text.append(description)

            event_json['url'] = url
            event_json['x'] = x
            event_json['y'] = y
            event_json['descriptions'] = descriptions_text    

            event_json['is_news'] = event.is_news

            response_json["event_" + str(event.id)] = event_json

        return JsonResponse(response_json)