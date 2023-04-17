import django.db.models
from django.utils.translation import gettext_lazy as _

import core.models
import tasks.managers
import teams.models


class Task(core.models.NameWithDetailAbstractModel):
    objects = tasks.managers.TasksManager()

    team = django.db.models.ForeignKey(
        to=teams.models.Team,
        verbose_name='команда',
        related_name='tasks',
        on_delete=django.db.models.CASCADE,
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='дата создания',
        help_text='когда создана команда?',
        auto_now_add=True,
    )
    deadline_date = django.db.models.DateTimeField(
        verbose_name='дата дедлайна',
        help_text='до какого времени надо сдать задачу?',
    )
    completed_date = django.db.models.DateTimeField(
        verbose_name='дата выполнения',
        help_text='когда была выполнена задача?',
        null=True,
    )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        default_related_name = 'task'

    def __str__(self):
        return self.name


class Meeting(core.models.NameWithDetailAbstractModel):
    team = django.db.models.ForeignKey(
        to=teams.models.Team,
        verbose_name='команда',
        related_name='meetings',
        on_delete=django.db.models.CASCADE,
    )
    planned_date = django.db.models.DateTimeField(
        verbose_name='дата встречи',
        help_text='когда пройдёт митап?',
    )
    status_choices = [
        (0, _('Ожидается')),
        (1, _('Идёт')),
        (2, _('Закончилась')),
    ]
    status = django.db.models.PositiveSmallIntegerField(
        verbose_name='статус',
        help_text='текущий статус встречи',
        choices=status_choices,
        default=0,
    )

    class Meta:
        verbose_name = 'встреча'
        verbose_name_plural = 'встречи'
        default_related_name = 'meeting'
