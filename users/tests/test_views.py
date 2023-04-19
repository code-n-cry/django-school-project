import django.db.utils
import django.urls
import mock
import pytz
from django.test import Client, TestCase, override_settings
from django.utils import timezone

import users.forms
import users.models


class ViewTests(TestCase):
    fixtures = ['skills_fixture.json', 'team_fixture.json']

    @classmethod
    def setUpClass(cls):
        cls.test_email = 'example@mail.com'
        cls.test_username = 'test_user'
        cls.test_password = '123'
        cls.test_signup_data = {
            'username': cls.test_username,
            'email': cls.test_email,
            'password1': cls.test_password,
            'password2': cls.test_password,
        }
        cls.test_login_data = {
            'username': cls.test_username,
            'password': cls.test_password,
        }
        super().setUpClass()

    def tearDown(self):
        users.models.User.objects.all().delete()
        super().tearDown()

    def test_invite_redirects_unauthorized(self):
        response = Client().get(django.urls.reverse('users:invites'))
        self.assertRedirects(
            response,
            ''.join(
                [
                    django.urls.reverse('auth:login'),
                    '?next=',
                    django.urls.reverse('users:invites'),
                ]
            ),
        )

    def test_profile_redirects_unauthorized(self):
        response = Client().get(django.urls.reverse('users:profile'))
        self.assertRedirects(
            response,
            ''.join(
                [
                    django.urls.reverse('auth:login'),
                    '?next=',
                    django.urls.reverse('users:profile'),
                ]
            ),
        )

    def test_send_request_redirects_unauthorized(self):
        response = Client().get(django.urls.reverse('users:send_request'))
        self.assertRedirects(
            response,
            ''.join(
                [
                    django.urls.reverse('auth:login'),
                    '?next=',
                    django.urls.reverse('users:send_request'),
                ]
            ),
        )

    def test_signup_context(self):
        response = Client().get(
            django.urls.reverse('auth:signup'),
        )
        self.assertIn('form', response.context)

    def test_profile_context(self):
        client = Client()
        users.models.User.objects.create_user(**self.test_login_data)
        client.login(**self.test_login_data)
        response = client.get(
            django.urls.reverse('users:profile'),
        )
        self.assertIn('form', response.context)
