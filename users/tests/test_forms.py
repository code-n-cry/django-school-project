from django.test import TestCase

import users.forms


class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile_form = users.forms.ProfileForm()
        cls.signup_form = users.forms.SignUpForm()
        cls.invite_form = users.forms.InviteForm()
        cls.request_form = users.forms.RequestForm()
        super().setUpClass()

    def test_labels(self):
        self.assertEqual(
            self.profile_form.fields['username'].label, 'Юзернейм'
        )
        self.assertEqual(self.profile_form.fields['first_name'].label, 'Имя')
        self.assertEqual(
            self.profile_form.fields['last_name'].label, 'Фамилия'
        )
        self.assertEqual(self.profile_form.fields['email'].label, 'E-mail')
        self.assertEqual(
            self.profile_form.fields['is_visible'].label, 'Видимость профиля'
        )
        self.assertEqual(self.profile_form.fields['avatar'].label, 'Аватар')
        self.assertEqual(self.signup_form.fields['username'].label, 'Юзернейм')
        self.assertEqual(self.signup_form.fields['password1'].label, 'Пароль')
        self.assertEqual(
            self.invite_form.fields['to_user'].label, 'Пользователю'
        )
        self.assertEqual(
            self.request_form.fields['to_team'].label, 'В команду:'
        )

    def test_help_texts(self):
        self.assertEqual(
            self.profile_form.fields['username'].help_text,
            'Имя, отображаемое на сайте',
        )
        self.assertEqual(
            self.profile_form.fields['first_name'].help_text,
            'Ваше имя(никто не увидит)',
        )
        self.assertEqual(
            self.profile_form.fields['last_name'].help_text,
            'Ваша фамилия(никто не увидит)',
        )
        self.assertEqual(
            self.profile_form.fields['email'].help_text, 'Ваш email'
        )
        self.assertEqual(
            self.profile_form.fields['is_visible'].help_text,
            'Будет ли видна информация о вас?',
        )
        self.assertEqual(
            self.profile_form.fields['avatar'].help_text,
            'Изображение в вашем профиле',
        )
        self.assertEqual(
            self.signup_form.fields['email'].help_text, 'Обязательное поле.'
        )
        self.assertEqual(
            self.invite_form.fields['to_user'].help_text,
            'Какого пользователя пригласить?',
        )
        self.assertEqual(
            self.request_form.fields['to_team'].help_text,
            'В какую команду запрос?',
        )
