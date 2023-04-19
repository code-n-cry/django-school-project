from django.contrib.auth import get_user_model
from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _

import core.forms
from tasks.models import Meeting, Task


class TaskCreationForm(core.forms.BaseTailwindModelForm):
    def __init__(self, team_id, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        self.fields[
            Task.users.field.name
        ].queryset = get_user_model().objects.filter(teams__in=[team_id])

    class Meta:
        model = Task
        fields = (
            Task.name.field.name,
            Task.detail.field.name,
            Task.deadline_date.field.name,
            Task.users.field.name,
        )
        labels = {
            Task.name.field.name: _('Название'),
            Task.detail.field.name: _('Описание'),
            Task.deadline_date.field.name: _('Дата дедлайна'),
            Task.users.field.name: _('Пользователи'),
        }
        help_texts = {
            Task.name.field.name: _('Как будет называться задача?'),
            Task.detail.field.name: _('Опишите задачу подробнее'),
            Task.deadline_date.field.name: _(
                'Дата, до которой надо выполнить задачу'
            ),
            Task.users.field.name: _('Кто будет выполнять задачу?'),
        }
        widgets = {
            Task.deadline_date.field.name: DateTimeInput(
                format=('%Y-%m-%d %H:%M'), attrs={'type': 'datetime-local'}
            )
        }


class MeetingCreationForm(core.forms.BaseTailwindModelForm):
    class Meta:
        model = Meeting
        fields = (
            Meeting.name.field.name,
            Meeting.detail.field.name,
            Meeting.planned_date.field.name,
        )
        labels = {
            Meeting.name.field.name: _('Тема'),
            Meeting.detail.field.name: _('Детали'),
            Meeting.planned_date.field.name: _('Дата'),
        }
        help_texts = {
            Meeting.name.field.name: _('Укажите тему встречи'),
            Meeting.detail.field.name: _(
                'Опишите подробнее, что будете обсуждать'
            ),
            Meeting.planned_date.field.name: _(
                'Дата, на которую будет назначена встреча'
            ),
        }
        widgets = {
            Meeting.planned_date.field.name: DateTimeInput(
                format=('%Y-%m-%d %H:%M'), attrs={'type': 'datetime-local'}
            )
        }
