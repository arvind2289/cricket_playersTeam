from django.db import models
from django.core.exceptions import ValidationError
import os
from uuid import uuid4
from django.utils.safestring import mark_safe


def validate_logo_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def validate_player_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0

    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def path_and_rename_logo(instance, filename):
    upload_to = 'logos/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


def path_and_rename_player(instance, filename):
    upload_to = 'player/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name or ''


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=path_and_rename_logo,
                             validators=[validate_logo_image], max_length=30,
                             help_text='Maximum file size allowed is 1Mb', default='')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name or ''


class Player(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    image = models.ImageField(upload_to=path_and_rename_player, max_length=30,
                              validators=[validate_player_image], help_text='Maximum file size allowed is 2Mb',
                              default='')
    jerseyNumber = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, max_length=30)
    matches = models.IntegerField(default=0)
    run = models.IntegerField(default=0)
    highest = models.IntegerField(default=0)
    fifties = models.IntegerField(default=0)
    hundreds = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='player_team')

    # def __str__(self):
    #     return self.team or ''


class Matches(models.Model):
    played_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    draw = models.BooleanField(default=False)



class MatchTeams(models.Model):
    MATCH_STATUS = (
        ('WON', 'WON'),
        ('DRAW', 'DRAW'),
        ('LOST', 'LOST'),
    )
    match = models.ForeignKey(Matches, on_delete=models.CASCADE, related_name="match")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="match_team")
    final_score = models.CharField(max_length=300, default="")
    winner = models.BooleanField(default=False)
    match_status = models.CharField(max_length=100, choices=MATCH_STATUS, default='')
    points = models.IntegerField(default=0)









class ScoreCard(models.Model):

    ACTION = WICKET = (
        ('BATSMAN', 'BATSMAN'),
        ('BOWLER', 'BOWLER'),
    )


    action = models.CharField(max_length=100, choices=ACTION, default='')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player', null=True, blank=True,
                               max_length=30)
    match = models.ForeignKey(Matches, on_delete=models.CASCADE, related_name='ScoreCardmatch', null=True, blank=True,
                              max_length=30)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='ScoreCardTeam', null=True, blank=True,
                              max_length=30)
    over = models.IntegerField(default=0)
    delivery = models.IntegerField(default=0)
    run = models.IntegerField(default=0)

    wicket =  models.BooleanField(default=False)

    wicket_of = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='wicket_of', null=True, blank=True,
                                  max_length=30)
    wicket_by = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='out_by', null=True, blank=True,
                               max_length=30)

