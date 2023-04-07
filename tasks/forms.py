import django.forms
from django.utils.translation import gettext_lazy as _

import tasks.models


class TaskCreationForm(django.forms.ModelForm):
    class Meta:
        model = tasks.models.Task
        fields = (
            tasks.models.Task.name.field.name,
            tasks.models.Task.detail.field.name,
            tasks.models.Task.to_users.field.name,
            tasks.models.Task.deadline_date.field.name,
        )
        labels = {
            tasks.models.Task.name.field.name: _('Название'),
            tasks.models.Task.detail.field.name: _('Описание'),
            tasks.models.Task.to_users.field.name: _('Пользователь(и)'),
            tasks.models.Task.deadline_date.field.name: _('Дедлайн'),
        }
        help_texts = {
            tasks.models.Task.name.field.name: _('Укажите название задачи'),
            tasks.models.Task.detail.field.name: _(
                'Опишите подробнее, что надо сделать'
            ),
            tasks.models.Task.to_users.field.name: _(
                'Кто будет выполнять задачу?'
            ),
            tasks.models.Task.deadline_date.field.name: _(
                'Дата, до которой надо выполнить задачу'
            ),
        }


class MeetingCreationForm(django.forms.ModelForm):
    class Meta:
        model = tasks.models.Meeting
        fields = (
            tasks.models.Meeting.name.field.name,
            tasks.models.Meeting.detail.field.name,
            tasks.models.Meeting.planned_date.field.name,
        )
        labels = {
            tasks.models.Meeting.name.field.name: _('Тема'),
            tasks.models.Meeting.detail.field.name: _('Детали'),
            tasks.models.Meeting.planned_date.field.name: _('Дата'),
        }
        help_texts = {
            tasks.models.Meeting.name.field.name: _('Укажите тему встречи'),
            tasks.models.Meeting.detail.field.name: _(
                'Опишите подробнее, что будете обсуждать'
            ),
            tasks.models.Meeting.planned_date.field.name: _(
                'Дата, на которую будет назначена встреча'
            ),
        }
