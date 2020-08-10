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
        player = models.Player.objects.get(user_id=request.user.id)
        descriptions = models.Description.objects.filter(player__id = player.id, event__id = event_id)
        
        if not descriptions:
            raise Http404("Вам недоступна данная информация")

        desc = descriptions.get(player_id = player.id, event_id=event_id)
        event_description = desc.information
        url = desc.event.image.file_field.url

        print(desc)
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
        player = models.Player.objects.get(user_id=request.user.id)
        descriptions = models.Description.objects.filter(player_id = player.id)
        game_time = models.Game.objects.get(id = request.COOKIES['game_id']).game_time
        response_json = {}
        for description in descriptions:
            if game_time >= description.event.time:
                print(description.event.time)
                event_json = {}
                event = description.event
                event_image = event.image
                json_event_name = 'event_'+ str(event.id)
                url = event_image.file_field.url
                x = event.pos_x
                y = event.pos_y
                description_text = description.information
                event_json['url'] = url
                event_json['x'] = x
                event_json['y'] = y
                event_json['description'] = description_text    
                event_json['is_news'] = event.is_news
                response_json["event_" + str(event.id)] = event_json
        return JsonResponse(response_json)