import django.db.models
import django.urls
from django.utils import timezone

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
        null=True,
    )
    planned_date = django.db.models.DateTimeField(
        verbose_name='дата встречи',
        help_text='когда пройдёт митап?',
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
