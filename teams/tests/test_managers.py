import django.test

import teams.models


class TestManagers(django.test.TestCase):
    fixtures = ('team_fixture.json',)

    def not_opened_teams_not_selected(self):
        opened_teams = teams.models.Team.objects.opened()
        self.assertEqual(
            len(opened_teams),
            1,
        )
