import django.db.models
from django.contrib.auth.models import AbstractUser

import teams.models


class User(AbstractUser):
    is_visible = django.db.models.BooleanField(
        default=True,
        verbose_name='статус видимости',
        help_text='могут ли другие пользователи звать вас в команды?',
    )
    lead = django.db.models.ForeignKey(
        teams.models.Team,
        on_delete=django.db.models.DO_NOTHING,
        null=True,
        verbose_name='управляемые команды',
        help_text='какими командами вы управляете?',
        related_name='lead',
    )
    members = django.db.models.ManyToManyField(
        teams.models.Team,
        verbose_name='команды',
        help_text='в каких команда вы состоите?',
        related_name='members',
    )
    invites = django.db.models.ForeignKey(
        teams.models.Invite,
        on_delete=django.db.models.CASCADE,
        verbose_name='приглашения',
        help_text='куда вас пригласили?',
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        default_related_name = 'user'
