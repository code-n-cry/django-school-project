from django.test import TestCase

import tasks.forms


class FormTest(TestCase):
    fixtures = ['skills_fixture.json', 'team_fixture.json']

    @classmethod
    def setUpClass(cls):
        cls.task_form = tasks.forms.TaskCreationForm(1)
        cls.meeting_form = tasks.forms.MeetingCreationForm()
        super().setUpClass()

    def test_labels(self):
        self.assertEqual(self.task_form.fields['name'].label, 'Название')
        self.assertEqual(self.task_form.fields['detail'].label, 'Описание')
        self.assertEqual(
            self.task_form.fields['deadline_date'].label, 'Дата дедлайна'
        )
        self.assertEqual(self.task_form.fields['users'].label, 'Пользователи')
        self.assertEqual(self.meeting_form.fields['name'].label, 'Тема')
        self.assertEqual(self.meeting_form.fields['detail'].label, 'Детали')
        self.assertEqual(
            self.meeting_form.fields['planned_date'].label, 'Дата'
        )

    def test_help_texts(self):
        self.assertEqual(
            self.task_form.fields['name'].help_text,
            'Как будет называться задача?',
        )
        self.assertEqual(
            self.task_form.fields['detail'].help_text,
            'Опишите задачу подробнее',
        )
        self.assertEqual(
            self.task_form.fields['deadline_date'].help_text,
            'Дата, до которой надо выполнить задачу',
        )
        self.assertEqual(
            self.task_form.fields['users'].help_text,
            'Кто будет выполнять задачу?',
        )
        self.assertEqual(
            self.meeting_form.fields['name'].help_text, 'Укажите тему встречи'
        )
        self.assertEqual(
            self.meeting_form.fields['detail'].help_text,
            'Опишите подробнее, что будете обсуждать',
        )
        self.assertEqual(
            self.meeting_form.fields['planned_date'].help_text,
            'Дата, на которую будет назначена встреча',
        )
