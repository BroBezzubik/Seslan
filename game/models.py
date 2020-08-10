from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import fields as post_fields

# Create your models here.

class Log(models.Model):
    file_name = models.CharField(max_length=50, null=False, verbose_name="Log file Name")
    file_path = models.CharField(default="Logs/",max_length=300, null=False)

    def __str__(self):
        return self.file_name


class Map(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Maps/")


class Game(models.Model):
    name = models.CharField(default="Seslan", max_length=30)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Date of Game")
    description = models.TextField(max_length=1000, verbose_name="Game description")
    log_id = models.OneToOneField(Log, on_delete=models.PROTECT)
    game_time = models.FloatField(default=0, null=False, verbose_name='In game time')
    map = models.ForeignKey(Map, default=None, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Proffesion(models.Model):
    proffesion_name = models.CharField(max_length=30, verbose_name='Proffesion')
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.proffesion_name


class Game_event_image(models.Model):
    file_name = models.CharField(max_length=30, verbose_name="Name of object image")
    file_field = models.ImageField(upload_to='Models')

    def __str__(self):
        return self.file_name


class Game_event(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(default="Some object", max_length=20)
    image = models.ForeignKey(Game_event_image, on_delete=models.PROTECT)
    time = models.FloatField(default=0)
    is_news = models.BooleanField(default=True)
    release = models.BooleanField(default=False)
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)

    def __str__(self):
        return self.name

  
class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    proffesion = models.ForeignKey(Proffesion, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username
    


class Information(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=2000)

    def __str__(self):
        return self.name
    


class Description(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.ForeignKey(Game_event, on_delete=models.CASCADE)
    information = models.ForeignKey(Information, on_delete=models.CASCADE)


