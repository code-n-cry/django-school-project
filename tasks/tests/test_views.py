import django.urls
from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    fixtures = [
        'skills_fixture.json',
        'team_fixture.json',
        'meeting_fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        test_user_data = {
            'username': 'test_username',
            'email': 'test@mail.com',
            'password': 'test123',
        }
        cls.test_user = get_user_model().objects.create_user(**test_user_data)
        super().setUpClass()

    def tearDown(self):
        get_user_model().objects.all().delete()
        super().tearDown()

    def test_meeting_detail_redirects_unauthorized_user(self):
        response = Client().get(
            django.urls.reverse('meetings:detail', kwargs={'pk': 1})
        )
        self.assertRedirects(
            response,
            ''.join(
                [
                    django.urls.reverse('auth:login'),
                    '?next=',
                    django.urls.reverse('meetings:detail', kwargs={'pk': 1}),
                ]
            ),
        )

    def test_task_create_redirects_unauthorized_users(self):
        response = Client().get(
            django.urls.reverse('tasks:create', kwargs={'team_id': 1})
        )
        self.assertRedirects(
            response,
            ''.join(
                [
                    django.urls.reverse('auth:login'),
                    '?next=',
                    django.urls.reverse('tasks:create', kwargs={'team_id': 1}),
                ]
            ),
        )
