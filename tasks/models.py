import django.db.models
from django.utils.translation import gettext_lazy as _

import core.models


class Task(core.models.NameWithDetailAbstractModel):
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
    planned_date = django.db.models.DateTimeField(
        verbose_name='дата встречи',
        help_text='когда пройдёт митап?',
    )
    status_choices = [
        (1, _('Ожидается')),
        (2, _('Идёт')),
        (3, _('Закончилась')),
    ]
    status = django.db.models.PositiveSmallIntegerField(
        verbose_name='статус',
        help_text='текущий статус встречи',
        choices=status_choices,
    )

    class Meta:
        verbose_name = 'встреча'
        verbose_name_plural = 'встречи'
        default_related_name = 'meeting'
