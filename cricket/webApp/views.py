from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View
from webApp.models import Team, Player, Matches, Country, ScoreCard, MatchTeams
from django.db.models import Count
import random
from django.db.models import Q
from django.forms.models import model_to_dict
from django.db.models import Sum


#
#
# # Create your views here.
#
#
class GetTeams(ListView):
    #### bulk this cominted code for create bulk team and player ####
    # strs = "player"
    #
    # for l in range(1,6):
    #     Country_instance = Country(
    #         name="Country" + str(l)
    #     )
    #     Country_instance.save()
    #     for j in range(1, 2):
    #         team = Team(
    #             name="Team" + Country_instance.name
    #             , logo="logos/90a492f82a24_aDJrXWE.jpg"
    #             , country=Country_instance
    #
    #         )
    #         team.save()
    #         playerCounter = 0
    #         for i in range(1, 11):
    #             playerCounter += 1
    #             str1 = team.name
    #             Player.objects.create(firstName=str1,
    #                                   lastName=strs + str(playerCounter),
    #                                   image='player/c6f8182c85e_XCmyTD2.jpg',
    #                                   jerseyNumber=i,
    #                                   country=Country_instance,
    #                                   matches=i,
    #                                   run=i, highest=i,
    #                                   hundreds=1 + i,
    #                                   team=team
    #                                   )
    #### end block bulk this cominted code for create bulk team and player ####


    context_object_name = 'team_list'
    template_name = "index.html"

    def get_queryset(self):
        return_obj = Team.objects.values("name").order_by(). \
                      annotate(wins=Count('match_team', filter=(Q(match_team__winner=True)))).\
            annotate(pionts=Sum('match_team__points'))
        #

        return list(return_obj.values("id","name","logo","wins","pionts" ))


class GetPlayers(ListView):
    context_object_name = 'player_list'
    template_name = "player.html"

    def get_queryset(self):
        return Player.objects.filter(team=self.kwargs['team_id'])


class GetMatch(View):
    def get(self, request):

        teams = random.sample(set(Team.objects.values_list('id')), 2)
        matchobj = Matches()
        matchobj.save()
        # print(teams)
        player_list = []
        MatchTeamsobjList = []
        for index, team in enumerate(teams):
            # print(team[0])
            team_obj = Team.objects.get(id=team[0])
            MatchTeamsobj = MatchTeams(match=matchobj, team=team_obj)
            MatchTeamsobj.save()
            MatchTeamsobjList.append(MatchTeamsobj)
            palyers = random.sample(set(Player.objects.filter(team=team[0]).values_list('id')), 10)
            player_list.append(list(map(lambda x: x[0], palyers)))
        score = [0, 0]

        for innings in range(1, 3):
            # print("inning is == ", innings)
            bowler = -1
            batsman = 0
            if innings == 1:
                batting_team = 0
                bowling_team = 1
            else:
                batting_team = 1
                bowling_team = 0
            for over in range(1, 21):

                for delivery in range(1, 7):
                    batsman_obj = Player.objects.get(id=player_list[batting_team][batsman])
                    bowler_obj = Player.objects.get(id=player_list[bowling_team][bowler])
                    action = random.randint(-1, 6)
                    if action == 5:
                        action = 4

                    if action < 0:
                        batting_ScoreCard = ScoreCard.objects.create(
                            player=batsman_obj,
                            team=batsman_obj.team,
                            match=matchobj,
                            over=over,
                            delivery=delivery,
                            wicket_by=bowler_obj,
                            wicket=True,
                            action="BATSMAN")
                        ScoreCard.objects.create(
                            player=bowler_obj,
                            team=bowler_obj.team,
                            match=matchobj,
                            over=over,
                            delivery=delivery,
                            wicket=True,
                            wicket_of=batsman_obj,
                            action="BOWLER")

                        if batsman == 9:
                            break
                        else:
                            # print("inning", innings, "Over", over, "delivery", delivery, "out batsman ->", batsman)
                            batsman += 1
                            if batsman == 9:
                                break
                    else:
                        score[innings - 1] = score[innings - 1] + action
                        ScoreCard.objects.create(
                            player=batsman_obj,
                            match=matchobj,
                            team=batsman_obj.team,
                            over=over,
                            delivery=delivery,
                            run=action,
                            action="BATSMAN")
                        ScoreCard.objects.create(
                            player=bowler_obj,
                            match=matchobj,
                            team=bowler_obj.team,
                            over=over,
                            delivery=delivery,
                            run=action,
                            action="BOWLER")
                        if innings == 2:
                            if score[1] > score[0]:
                                print("winner")
                                break

                if batsman == 9:
                    break
                if score[1] > score[0]:
                    print("winner")
                    break
                if over == 5 or over == 10 or over == 15:
                    bowler = -1
                bowler -= 1

            MatchTeamsobjList[innings - 1].final_score = str(score[innings - 1]) + "/" + str(batsman) + "(" + str(
                over) + "." + str(delivery) + ")"
            MatchTeamsobjList[innings - 1].save()

        if score[0] > score[1]:
            MatchTeamsobjList[0].winner = True
            MatchTeamsobjList[0].points = 2
            MatchTeamsobjList[0].save()
            match_result = MatchTeamsobjList[0].team.name + " won by " + str(score[0] - score[1]) + " runs "
        elif score[0] < score[1]:
            MatchTeamsobjList[1].winner = True
            MatchTeamsobjList[1].points = 2
            MatchTeamsobjList[1].save()
            match_result = MatchTeamsobjList[1].team.name + " won by " + str(9 - batsman) + " wickets"

            print(MatchTeamsobjList[1])
        else:
            matchobj.draw = True
            matchobj.save()
            MatchTeamsobjList[0].points = 1
            MatchTeamsobjList[1].points = 1
            MatchTeamsobjList[0].save()
            MatchTeamsobjList[1].save()
            match_result = "Match draw"

        MatchTeamsobjList[0] = model_to_dict(MatchTeamsobjList[0])
        MatchTeamsobjList[1] = model_to_dict(MatchTeamsobjList[1])

        for MatchTeamsobj in MatchTeamsobjList:
            bat_inning = ScoreCard.objects.filter(team=MatchTeamsobj["team"],
                                                  match=MatchTeamsobj["match"],
                                                  action="BATSMAN").values("player_id").order_by(
            ).annotate(total_run=Sum('run')
                       ).annotate(six=Count('player_id', filter=Q(run=6))
                                  ).annotate(four=Count('player_id', filter=Q(run=4))
                                             ).annotate(balls=Count('player_id'))

            MatchTeamsobj["bat_inning"] = list(bat_inning.values("player__firstName",
                                                                 "player__lastName",
                                                                 "player__image",
                                                                 "player__firstName",
                                                                 "total_run", "four", "six", "balls"))

            ball_inning = ScoreCard.objects.filter(team=MatchTeamsobj["team"],
                                                   match=MatchTeamsobj["match"],
                                                   action="BOWLER").values("player_id").order_by(
            ).annotate(total_run=Sum('run')
                       ).annotate(total_run=Sum('run')
                                  ).annotate(wickets=Count('player_id', filter=Q(wicket=True))
                                             ).annotate(overs=Count('player_id') / 6
                                                        ).annotate(balls=Count('player_id')
                                                                   ).annotate(subover=Count('player_id') % 6)

            MatchTeamsobj["ball_inning"] = list(
                ball_inning.values("player__firstName", "player__lastName", "player__image", "player__firstName",
                                   "total_run", "wickets", "balls", "overs", "subover"))

            MatchTeamsobj["team__name"] = list(
                ball_inning.values("player__team__name"))[0]["player__team__name"]

        return render(request, 'match.html', {"match": model_to_dict(matchobj),
                                              "scores": MatchTeamsobjList,
                                              "match_result": match_result})
