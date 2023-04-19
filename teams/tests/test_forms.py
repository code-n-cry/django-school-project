from django.test import TestCase

import teams.forms


class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.form = teams.forms.TeamForm()
        super().setUpClass()

    def test_labels(self):
        self.assertEqual(self.form.fields['name'].label, 'Название')
        self.assertEqual(self.form.fields['detail'].label, 'Описание')
        self.assertEqual(self.form.fields['is_open'].label, 'Открытая?')
        self.assertEqual(self.form.fields['avatar'].label, 'Аватарка')
        self.assertEqual(self.form.fields['skills'].label, 'Навыки(тэги)')

    def test_help_texts(self):
        self.assertEqual(
            self.form.fields['name'].help_text, 'Как будет называться команда?'
        )
        self.assertEqual(
            self.form.fields['detail'].help_text,
            'Расскажите о команде подробнее.',
        )
        self.assertEqual(
            self.form.fields['is_open'].help_text,
            'Будет ли показываться команда всем пользователям?',
        )
        self.assertEqual(
            self.form.fields['avatar'].help_text,
            'Профильное изображение команды',
        )
        self.assertEqual(
            self.form.fields['skills'].help_text,
            'Что должен уметь участник команды?',
        )
