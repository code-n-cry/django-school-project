import django.urls
from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class ViewTests(TestCase):
    fixtures = ['skills_fixture.json', 'team_fixture.json']

    @classmethod
    def setUpClass(cls):
        cls.test_user_data = {
            'username': 'test username',
            'password': '123',
        }
        cls.user = get_user_model().objects.create_user(**cls.test_user_data)
        super().setUpClass()

    def tearDown(self):
        get_user_model().objects.all().delete()
        super().tearDown()

    def test_calendar_not_in_unauthorized_user_context(self):
        response = Client().get(django.urls.reverse('homepage:home'))
        self.assertNotIn('calendar', response.context)

    def test_lead_teams_not_in_unauthorized_user_context(self):
        response = Client().get(django.urls.reverse('homepage:home'))
        self.assertNotIn('lead_teams', response.context)

    def test_teams_not_in_unauthorized_user_context(self):
        response = Client().get(django.urls.reverse('homepage:home'))
        self.assertNotIn('other_teams', response.context)

    def test_opened_teams_in_unauthorized_user_context(self):
        response = Client().get(django.urls.reverse('homepage:home'))
        self.assertIn('opened_teams', response.context)

    def test_calendar_in_authorized_user_context(self):
        client = Client()
        client.login(**self.test_user_data)
        response = client.get(django.urls.reverse('homepage:home'))
        self.assertIn('calendar', response.context)

    def test_lead_teams_in_authorized_user_context(self):
        client = Client()
        client.login(**self.test_user_data)
        response = client.get(django.urls.reverse('homepage:home'))
        self.assertIn('lead_teams', response.context)

    def test_teams_in_authorized_user_context(self):
        client = Client()
        client.login(**self.test_user_data)
        response = client.get(django.urls.reverse('homepage:home'))
        self.assertIn('other_teams', response.context)
