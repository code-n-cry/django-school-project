from django.test import TestCase

import skills.forms


class FormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_form = skills.forms.SkillCreationForm()
        super().setUpClass()

    def test_labels(self):
        self.assertEqual(self.skill_form.fields['name'].label, 'Название')

    def test_help_texts(self):
        self.assertEqual(
            self.skill_form.fields['name'].help_text,
            'Укажите название навыка(уникальное, не больше 25 символов)',
        )
