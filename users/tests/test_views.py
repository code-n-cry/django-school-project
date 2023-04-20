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
        cls.test_password = 'test!password123'
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

    def test_correct_signup(self):
        users_count = users.models.User.objects.count()
        Client().post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        self.assertTrue(
            users.models.User.objects.filter(
                email=self.test_email,
            ).exists()
        )
        self.assertEqual(users.models.User.objects.count(), users_count + 1)

    def test_signup_normalizing_email(self):
        users_count = users.models.User.objects.count()
        data = {
            'username': self.test_username + 's',
            'email': self.test_email.upper(),
            'password1': self.test_password,
            'password2': self.test_password,
        }
        Client().post(
            django.urls.reverse('auth:signup'),
            data=data,
            follow=True,
        )
        self.assertTrue(
            users.models.User.objects.filter(
                email=self.test_email,
            ).exists()
        )
        self.assertEqual(users.models.User.objects.count(), users_count + 1)

    def test_signup_no_username(self):
        users_count = users.models.User.objects.count()
        invalid_signup_data = {
            'email': self.test_email,
            'password1': self.test_password,
            'password2': self.test_password,
        }
        Client().post(
            django.urls.reverse('auth:signup'),
            data=invalid_signup_data,
            follow=True,
        )
        self.assertFalse(
            users.models.User.objects.filter(
                email=self.test_email,
            ).exists()
        )
        self.assertEqual(users.models.User.objects.count(), users_count)

    def test_signup_no_email(self):
        users_count = users.models.User.objects.count()
        invalid_signup_data = {
            'username': self.test_username,
            'password1': self.test_password,
            'password2': self.test_password,
        }
        Client().post(
            django.urls.reverse('auth:signup'),
            data=invalid_signup_data,
            follow=True,
        )
        self.assertEqual(users.models.User.objects.count(), users_count)

    def test_signup_passwords_dont_match(self):
        users_count = users.models.User.objects.count()
        invalid_signup_data = {
            'username': self.test_username,
            'email': self.test_email,
            'password1': self.test_password,
            'password2': self.test_password + 's',
        }
        Client().post(
            django.urls.reverse('auth:signup'),
            data=invalid_signup_data,
            follow=True,
        )
        self.assertEqual(users.models.User.objects.count(), users_count)

    def test_signup_with_not_unique_email(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        users_count = users.models.User.objects.count()
        new_signup_data = {
            'username': self.test_username + 's',
            'email': self.test_email,
            'password1': self.test_password,
            'password2': self.test_password,
        }
        client.post(
            django.urls.reverse('auth:signup'),
            data=new_signup_data,
            follow=True,
        )
        self.assertEqual(users.models.User.objects.count(), users_count)

    @override_settings(USER_ACTIVE_DEFAULT=False)
    def test_activate_works_for_new_user(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        client.get(
            django.urls.reverse(
                'auth:activate_new', kwargs={'username': self.test_username}
            )
        )
        self.assertTrue(
            users.models.User.objects.filter(username=self.test_username)
            .first()
            .is_active
        )

    @override_settings(USER_ACTIVE_DEFAULT=False)
    @mock.patch('django.utils.timezone.now')
    def test_activate_doesnt_work_within_twelve_hours(self, mock_now):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        utc = pytz.UTC
        mock_now.return_value = utc.localize(timezone.datetime(2024, 4, 1))
        client.get(
            django.urls.reverse(
                'auth:activate_new', kwargs={'username': self.test_username}
            )
        )
        self.assertFalse(
            users.models.User.objects.filter(
                username=self.test_username
            ).exists()
        )

    def test_login_with_username(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        credentials = {
            'username': self.test_username,
            'password': self.test_password,
        }
        response = client.post(
            django.urls.reverse('auth:login'),
            data=credentials,
            follow=True,
        )
        self.assertTrue(response.context['user'].is_active)

    def test_login_with_email(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        credentials = {
            'username': self.test_email,
            'password': self.test_password,
        }
        response = client.post(
            django.urls.reverse('auth:login'),
            data=credentials,
            follow=True,
        )
        self.assertTrue(response.context['user'].is_active)

    def test_login_with_not_normalized_email(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        email = 'example+tag@mail.com'
        credentials = {
            'username': email,
            'password': self.test_password,
        }
        response = client.post(
            django.urls.reverse('auth:login'),
            data=credentials,
            follow=True,
        )
        self.assertTrue(response.context['user'].is_active)

    @override_settings(MAX_LOGIN_AMOUNT=1)
    def test_login_block(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        credentials = {
            'username': self.test_email,
            'password': self.test_password + 'wrong',
        }
        response = client.post(
            django.urls.reverse('auth:login'),
            data=credentials,
            follow=True,
        )
        self.assertFalse(response.context['user'].is_active)

    @override_settings(MAX_LOGIN_AMOUNT=1)
    def test_login_block_recovery(self):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        credentials = {
            'username': self.test_email,
            'password': self.test_password + 'wrong',
        }
        response = client.post(
            django.urls.reverse('auth:login'),
            data=credentials,
            follow=True,
        )
        self.assertFalse(response.context['user'].is_active)
        response = client.get(
            django.urls.reverse(
                'auth:recover', kwargs={'username': self.test_username}
            )
        )
        self.assertTrue(
            users.models.User.objects.filter(username=self.test_username)
            .first()
            .is_active
        )

    @override_settings(MAX_LOGIN_AMOUNT=1)
    @mock.patch('django.utils.timezone.now')
    def test_login_block_recovery_doesnt_work_within_week(self, mock_now):
        client = Client()
        client.post(
            django.urls.reverse('auth:signup'),
            data=self.test_signup_data,
            follow=True,
        )
        utc = pytz.UTC
        mock_now.return_value = utc.localize(timezone.datetime(2023, 3, 20))
        credentials = {
            'username': self.test_email,
            'password': self.test_password + 'wrong',
        }
        client.login(
            **credentials,
        )
        mock_now.return_value = utc.localize(timezone.datetime(2023, 3, 31))
        client.get(
            django.urls.reverse(
                'auth:recover', kwargs={'username': self.test_username}
            )
        )
        self.assertFalse(
            users.models.User.objects.filter(
                username=self.test_username
            ).exists()
        )
