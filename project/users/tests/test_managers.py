import django.test

import users.managers
import users.models


class ManagerTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_username = 'username'
        cls.yandex_domain_long = '@yandex.ru'
        cls.yandex_domain_short = '@ya.ru'
        cls.google_domain = '@gmail.com'
        cls.active_user_data = {
            'username': 'test',
            'email': 'test@mail.com',
            'is_active': True,
            'password': '123',
            'is_visible': True,
        }
        cls.inactive_user_data = {
            'username': 'test',
            'email': 'test@mail.com',
            'is_active': False,
            'password': '123',
            'is_visible': True,
        }
        super().setUpClass()

    def tearDown(self):
        users.models.User.objects.all().delete()
        super().tearDown()

    def test_ignore_tags(self):
        test_tags = ['+tag', '+test']
        self.assertEqual(
            users.managers.ActiveUserManager.normalize_email(
                self.test_username
                + ''.join(test_tags)
                + self.yandex_domain_long,
            ),
            self.test_username + self.yandex_domain_long,
        )
        self.assertEqual(
            users.managers.ActiveUserManager.normalize_email(
                self.test_username + ''.join(test_tags) + self.google_domain,
            ),
            self.test_username + self.google_domain,
        )

    def test_no_register(self):
        self.assertEqual(
            users.managers.ActiveUserManager.normalize_email(
                self.test_username.upper() + self.yandex_domain_long.upper()
            ),
            self.test_username + self.yandex_domain_long,
        )

    def test_canonize_yandex_domen(self):
        self.assertEqual(
            users.managers.ActiveUserManager.normalize_email(
                self.test_username + self.yandex_domain_short
            ),
            users.managers.ActiveUserManager.normalize_email(
                self.test_username + self.yandex_domain_long
            ),
        )

    def test_dots_replacing_yandex_domen(self):
        test_mail_username = 'example.test.email'
        self.assertEqual(
            users.managers.ActiveUserManager.normalize_email(
                test_mail_username + self.yandex_domain_long
            ),
            test_mail_username.replace('.', '-') + self.yandex_domain_long,
        )

    def test_gmail_ignore_dots(self):
        test_mail_username = 'example.test.email'
        self.assertEqual(
            users.managers.ActiveUserManager.normalize_email(
                test_mail_username + self.google_domain
            ),
            test_mail_username.replace('.', '') + self.google_domain,
        )

    def test_active_user_selected(self):
        test_user = users.models.User.objects.create_user(
            **self.active_user_data,
        )
        active_users = users.models.User.objects.active()
        self.assertIn(
            test_user,
            active_users,
        )

    def test_inactive_user_not_selected(self):
        test_user = users.models.User.objects.create_user(
            **self.inactive_user_data,
        )
        active_users = users.models.User.objects.active()
        self.assertNotIn(
            test_user,
            active_users,
        )

    def test_active_public_user_selected(self):
        test_user = users.models.User.objects.create_user(
            **self.active_user_data,
        )
        public_users = users.models.User.objects.public()
        self.assertIn(
            test_user,
            public_users,
        )

    def test_active_not_public_user_not_selected(self):
        test_user = users.models.User.objects.create_user(
            username='test', password='123', is_visible=False
        )
        public_users = users.models.User.objects.public()
        self.assertNotIn(
            test_user,
            public_users,
        )

    def test_inactive_public_user_not_selected(self):
        test_user = users.models.User.objects.create_user(
            **self.inactive_user_data,
        )
        public_users = users.models.User.objects.public()
        self.assertNotIn(
            test_user,
            public_users,
        )
