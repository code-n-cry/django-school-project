import django.forms
from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _

import core.forms
from tasks.models import Meeting, Task
from users.models import User


class TaskCreationForm(core.forms.BaseTailwindModelForm):
    def __init__(self, team_id, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        self.fields[Task.users.field.name].queryset = User.objects.filter(
            teams__in=[team_id]
        )

    users = django.forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label=Task.users.field.verbose_name,
        help_text=_('Кто будет выполнять задачу?'),
    )

    class Meta:
        model = Task
        fields = (
            Task.name.field.name,
            Task.detail.field.name,
            Task.deadline_date.field.name,
        )
        help_texts = {
            Task.deadline_date.field.name: _(
                'Дата, до которой надо выполнить задачу'
            ),
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
