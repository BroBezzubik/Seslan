from django.contrib import admin
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
from .models import Log, Game, Proffesion, Game_event_image, Game_event, Player

@admin.register(Log, Game, Proffesion, Game_event_image, Game_event, Player)
class SeslanAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget}
    }

