import django.db.models
import django.urls
from django.contrib.auth import get_user_model

import core.models
import tasks.managers
import teams.models


class Task(core.models.NameWithDetailAbstractModel):
    objects = tasks.managers.TasksManager()

    completed_date = django.db.models.DateTimeField(
        verbose_name='дата выполнения',
        help_text='когда была выполнена задача?',
        null=True,
    )
    team = django.db.models.ForeignKey(
        to=teams.models.Team,
        verbose_name='команда',
        related_name='tasks',
        on_delete=django.db.models.CASCADE,
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='дата создания',
        help_text='когда создано задание?',
        auto_now_add=True,
    )
    deadline_date = django.db.models.DateTimeField(
        verbose_name='дата дедлайна (формат: год-месяц-день)',
        help_text='до какого времени надо сдать задачу?',
    )
    users = django.db.models.ManyToManyField(
        to=get_user_model(),
        verbose_name='Пользователи',
        related_name='tasks',
        blank=True,
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

    class Meta:
        verbose_name = 'встреча'
        verbose_name_plural = 'встречи'
        default_related_name = 'meeting'
