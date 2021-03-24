from django.test import SimpleTestCase
from django.urls import reverse, resolve
from webApp.views import GetTeams, GetPlayers

class TestUrls(SimpleTestCase):

    def team_list_url_is_resolved(self):
        url = reverse('team_list')
        self.assertEqual(resolve(url).func.view_class, GetTeams)


    def player_list_url_is_resolved(self):
        url = reverse('play_list')

        self.assertEqual(resolve(url).func.view_class, GetTeams)

