from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import fields as post_fields

# Create your models here.

class Log(models.Model):
    file_name = models.CharField(max_length=50, null=False, verbose_name="Log file Name")
    file_field = models.FileField(upload_to='Game logs/%Y/%m/%d/')


class Game(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Date of Game")
    description = models.TextField(max_length=1000, verbose_name="Game description")
    log_id = models.OneToOneField(Log, on_delete=models.PROTECT)


class Proffesion(models.Model):
    proffesion_name = models.CharField(max_length=30, verbose_name=Proffesion)
    description = models.TextField(max_length=500)


class Object_image(models.Model):
    file_name = models.CharField(max_length=30, verbose_name="Name of object image")
    file_field = models.FileField('Models/')


class Object(models.Model):
    image = models.ForeignKey(Object_image, on_delete=models.PROTECT)
    information = post_fields.JSONField()


class Player(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.PROTECT)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    proffesion = models.OneToOneField(Proffesion, on_delete=models.PROTECT)
    permissions = post_fields.JSONField()
    objects = models.ManyToManyField(Object)




