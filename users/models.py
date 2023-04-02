import django.db.models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    team_invites = django.db.models.ForeignKey(
        'invite',
        on_delete=django.db.models.CASCADE,
        verbose_name='приглашения',
        help_text='приглашения пользователя в команды',
    )
    teams = django.db.models.ManyToManyField(
        'team',
        on_delete=django.db.models.DO_NOTHING,
        verbose_name='команды',
        help_text='список команд, в которых вы состоите',
    )
    is_visible = django.db.models.BooleanField(
        default=True,
        verbose_name='статус видимости',
        help_text='могут ли другие пользователи звать вас в команды?',
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        default_related_name = 'user'
