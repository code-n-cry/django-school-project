import django.db.models

import tasks.models


class Team(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name='название команды',
        help_text='как будет называться команда?',
        max_length=150,
        unique=True,
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='дата создания',
        help_text='когда создана команда?',
        auto_now_add=True,
    )
    tasks = django.db.models.ForeignKey(
        tasks.models.Task,
        on_delete=django.db.models.CASCADE,
        verbose_name='задания',
        help_text='задания для команды',
    )
    is_open = django.db.models.BooleanField(
        default=True,
        verbose_name='открытость',
        help_text='показывается ли ваша команда в поиске?',
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
