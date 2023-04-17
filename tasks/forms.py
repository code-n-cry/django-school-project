from django.forms.widgets import DateTimeInput
from django.utils.translation import gettext_lazy as _

from core.forms import BaseTailwindModelForm
from tasks.models import Meeting, Task


class TaskCreationForm(BaseTailwindModelForm):
    class Meta:
        model = Task
        fields = (
            Task.name.field.name,
            Task.detail.field.name,
            Task.deadline_date.field.name,
        )
        labels = {
            Task.name.field.name: _('Название'),
            Task.detail.field.name: _('Описание'),
            Task.deadline_date.field.name: _('Дедлайн'),
        }
        help_texts = {
            Task.name.field.name: _('Укажите название задачи'),
            Task.detail.field.name: _('Опишите подробнее, что надо сделать'),
            Task.deadline_date.field.name: _(
                'Дата, до которой надо выполнить задачу'
            ),
        }


class MeetingCreationForm(BaseTailwindModelForm):
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
