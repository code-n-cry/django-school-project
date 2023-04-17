import django.db.models
import django.urls
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import core.models
import tasks.managers
import users.models


class Task(core.models.NameWithDetailAbstractModel):
    objects = tasks.managers.TasksManager()

    completed_date = django.db.models.DateTimeField(
        verbose_name='дата выполнения',
        help_text='когда была выполнена задача?',
        null=True,
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='дата создания',
        help_text='когда создано задание?',
        auto_now_add=True,
    )
    deadline_date = django.db.models.DateTimeField(
        verbose_name='дата дедлайна',
        help_text='до какого времени надо сдать задачу?',
    )
    users = django.db.models.ManyToManyField(
        users.models.User,
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

    @property
    def get_html_paragraph(self):
        planned_date = timezone.localtime(self.planned_date)
        planned_date = planned_date.strftime('%H:%M')
        meeting_link = django.urls.reverse(
            'meetings:detail', kwargs={'pk': self.pk}
        )
        style = 'underline text-blue-600 hover:text-blue-800'
        html_content = [
            f'<p class="text-white text-center">{planned_date} ',
            f'<a class="{style}" href="{meeting_link}">{self.name}</a></p>',
        ]
        return ''.join(html_content)
