import datetime
from http import HTTPStatus

import django.urls
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

import teams.models
import users.models


class StaticUrlTests(TestCase):
    fixtures = [
        'skills_fixture.json',
        'team_fixture.json',
        'meeting_fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.test_user_data = {
            'username': 'test_username',
            'password': 'test123',
        }
        cls.test_user = get_user_model().objects.create_user(
            **cls.test_user_data
        )
        cls.form_data = {
            'name': ['test task'],
            'detail': ['test task'],
            'deadilne_date': [
                datetime.datetime(2030, 4, 17, 17, 43).strftime(
                    '%Y-%m-%d %H:%M'
                )
            ],
            'users': [str(cls.test_user.pk)],
        }
        super().setUpClass()

    def tearDown(self):
        get_user_model().objects.all().delete()
        users.models.Member.objects.all().delete()
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

    def test_your_meetings_redirects_unauthorized_users(self):
        response = Client().get(django.urls.reverse('meetings:yours'))
        self.assertRedirects(
            response,
            ''.join(
                [
                    django.urls.reverse('auth:login'),
                    '?next=',
                    django.urls.reverse('meetings:yours'),
                ]
            ),
        )

    def test_meeting_detail_redirects_not_team_member(self):
        client = Client()
        client.login(**self.test_user_data)
        response = client.get(
            django.urls.reverse('meetings:detail', kwargs={'pk': 1})
        )
        self.assertRedirects(response, django.urls.reverse('homepage:home'))

    def test_meeting_detail_work_with_team_member(self):
        client = Client()
        client.login(**self.test_user_data)
        users.models.Member.objects.create(
            user=self.test_user, team=teams.models.Team.objects.get(pk=1)
        )
        response = client.get(
            django.urls.reverse('meetings:detail', kwargs={'pk': 1})
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )

    def test_task_redirects_not_lead(self):
        client = Client()
        client.login(**self.test_user_data)
        users.models.Member.objects.create(
            user=self.test_user, team=teams.models.Team.objects.get(pk=1)
        )
        response = client.get(
            django.urls.reverse('tasks:create', kwargs={'team_id': 1})
        )
        self.assertRedirects(response, django.urls.reverse('homepage:home'))
