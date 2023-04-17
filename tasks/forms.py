import django.forms
from django.utils.translation import gettext_lazy as _

import core.forms
import tasks.models
import users.models


class TaskCreationForm(core.forms.BaseTailwindModelForm):
    def __init__(self, team_id, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        self.fields[
            tasks.models.Task.users.field.name
        ].queryset = users.models.User.objects.filter(teams__in=[team_id])

    users = django.forms.ModelMultipleChoiceField(
        queryset=users.models.User.objects.all(),
        label=tasks.models.Task.users.field.verbose_name,
        help_text=_('Кто будет выполнять задачу?'),
    )

    class Meta:
        model = tasks.models.Task
        fields = (
            tasks.models.Task.name.field.name,
            tasks.models.Task.detail.field.name,
            tasks.models.Task.deadline_date.field.name,
        )
        help_texts = {
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
