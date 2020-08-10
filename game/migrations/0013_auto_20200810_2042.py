# Generated by Django 3.0.9 on 2020-08-10 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20200809_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.Game_event'),
        ),
        migrations.AlterField(
            model_name='description',
            name='player',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.Player'),
        ),
    ]
