from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('select_game', views.select_game, name='select_game'),
    
    path('game/<int:game_id>', views.game, name='game'),
    path('game/event_info/<int:event_id>', views.event_info),
    
    path(r'game/ajax_get_game_map', views.ajax_get_game_map),
    path(r'game/ajax_update_events', views.ajax_update_events),
    path(r'game/ajax_get_url_info_event_<int:event_id>', views. ajax_get_url_event_info),
]