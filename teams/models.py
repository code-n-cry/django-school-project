import django.db.models
from django.utils import timezone

import core.models
from tasks.models import Task, Meeting


def avatar_image_path(instance, filename):
    return f'uploads/teams/{instance.id}-{timezone.now()}/{filename}'


class Team(core.models.UniqueNameWithDetailAbstractModel):
    created_at = django.db.models.DateTimeField(
        verbose_name='дата создания',
        help_text='когда создана команда?',
        auto_now_add=True,
    )
    tasks = django.db.models.ForeignKey(
        Task,
        on_delete=django.db.models.CASCADE,
        verbose_name='задания',
        help_text='задания для команды',
    )
    meetings = django.db.models.ForeignKey(
        to=Meeting,
        on_delete=django.db.models.CASCADE,
        verbose_name='встречи',
        help_text='запланированные командные встречи',
    )
    is_open = django.db.models.BooleanField(
        default=True,
        verbose_name='открытость',
        help_text='показывается ли ваша команда в поиске?',
    )
    avatar = django.db.models.ImageField(
        upload_to=avatar_image_path,
        verbose_name='аватарка',
        help_text='картинка профиля команды',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'
        default_related_name = 'team'


class Invite(django.db.models.Model):
    to_team = django.db.models.ForeignKey(
        Team,
        on_delete=django.db.models.CASCADE,
        verbose_name='команда',
        help_text='в какую команду приглашение?',
    )

    class Meta:
        verbose_name = 'приглашение'
        verbose_name_plural = 'приглашения'
        default_related_name = 'invite'

    def __str__(self):
        return f'Приглашение в команду {self.to_team.name.field}'
