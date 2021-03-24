from django.contrib import admin
from .models import Team, Player, Matches,Country, ScoreCard, MatchTeams
from django.utils.html import format_html


# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    fields = ['name', 'logo', 'country']
    list_display = ['name', 'logo', 'country']


admin.site.register(Team, TeamAdmin)
#

class PlayerAdmin(admin.ModelAdmin):
    list_display = ["team", "firstName", "lastName", "image", "jerseyNumber",
                    "country", "matches", "run", "highest", "fifties", "hundreds"]
    #list_display = __all__


admin.site.register(Player, PlayerAdmin)
#
#
class MatchesAdmin(admin.ModelAdmin):
    # list_display = ['id', 'team']
    pass


admin.site.register(Matches, MatchesAdmin)


class ScoreCardAdmin(admin.ModelAdmin):
    list_display = ["action","player","match","over","delivery","run","wicket","wicket_of","wicket_by"]



admin.site.register(ScoreCard, ScoreCardAdmin)

class MatchTeamsAdmin(admin.ModelAdmin):
    list_display = [
        "match",
        "team",
        "final_score",
        "winner"
    ]



admin.site.register(MatchTeams, MatchTeamsAdmin)

#
#


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Country, CountryAdmin)