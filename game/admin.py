from django.contrib import admin
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
from .models import Log, Game, Proffesion, Game_event_image, Game_event, Player, Map, Description

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'date',
        'log_id'
    ]


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = [
        'player',
        'event',
    ]


@admin.register(Game_event_image)
class EventImageAdmin(admin.ModelAdmin):
    list_display = [
        'file_name'
    ]


@admin.register(Game_event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image',
        'time',
    ]


@admin.register(Player)
class SeslanAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget}
    }

