import time

import django.db.models
import django.utils.html
import sorl
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static
from django.utils.translation import gettext_lazy

import skills.models
import teams.models
import users.managers
from tasks.models import Task


def avatar_image_path(instance, filename):
    return f'uploads/{instance.id}-{time.strftime("%Y%m%d-%H%M%S")}/{filename}'


class User(AbstractUser):
    objects = users.managers.ActiveUserManager()

    detail = django.db.models.TextField(
        null=True,
        max_length=550,
        verbose_name='детали',
        help_text='расскажите о себе детальнее',
    )
    is_visible = django.db.models.BooleanField(
        default=True,
        verbose_name='статус видимости',
        help_text='могут ли другие пользователи звать вас в команды?',
    )
    avatar = django.db.models.ImageField(
        upload_to=avatar_image_path,
        verbose_name='аватарка',
        help_text='картинка профиля пользователя',
        null=True,
        blank=True,
    )
    skills = django.db.models.ManyToManyField(
        to=skills.models.Skill,
        verbose_name='навыки',
        help_text='Ваши навыки',
        blank=True,
    )
    tasks = django.db.models.ManyToManyField(
        Task,
        verbose_name='задачи',
        help_text='задачи, назначенные вам',
        related_name='to_users',
        blank=True,
    )
    failed_logins = django.db.models.IntegerField(
        verbose_name='количество неудачных входов с момента удачного',
        help_text='сколько раз был провален вход в аккаунт',
        default=0,
    )
    last_failed_login_date = django.db.models.DateTimeField(
        verbose_name='дата последней неудачной попытки входа',
        null=True,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        default_related_name = 'user'

    def get_avatar_300x300(self):
        if self.avatar:
            return sorl.thumbnail.get_thumbnail(
                self.avatar, '300x300', crop='center', quality=65
            )

        return {'url': static('img/default.jpg')}

    def avatar_tmb(self):
        if self.avatar:
            return django.utils.html.mark_safe(
                f'<img src="{self.get_avatar_300x300().url}">'
            )
        self.avatar_tmb.short_description = 'превью'
        return gettext_lazy('Нет аватарки')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            self.avatar = self.get_avatar_300x300()

    def __str__(self):
        return self.username


class Member(django.db.models.Model):
    is_lead = django.db.models.BooleanField(
        default=False,
        verbose_name='лид',
        help_text='является ли участник лидом',
    )
    team = django.db.models.ForeignKey(
        teams.models.Team,
        verbose_name='команда',
        help_text='команда, в которой состоит юзер',
        on_delete=django.db.models.CASCADE,
        related_name='members',
    )
    user = django.db.models.ForeignKey(
        User,
        verbose_name='пользователь',
        help_text='юзер',
        on_delete=django.db.models.CASCADE,
        related_name='teams',
    )

    class Meta:
        constraints = [
            django.db.models.UniqueConstraint(
                name='unique_member', fields=['team', 'user']
            )
        ]
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
        default_related_name = 'member'


class Invite(django.db.models.Model):
    from_team = django.db.models.ForeignKey(
        to=teams.models.Team,
        on_delete=django.db.models.CASCADE,
        verbose_name='команда',
        help_text='в какую команду приглашение?',
    )
    to_user = django.db.models.ForeignKey(
        to=User,
        on_delete=django.db.models.DO_NOTHING,
        verbose_name='пользователь',
        help_text='какому пользователю приглашение?',
    )

    class Meta:
        verbose_name = 'приглашение'
        verbose_name_plural = 'приглашения'
        default_related_name = 'invite'

    def __str__(self):
        return f'Приглашение в команду {self.from_team.name}'


class Request(django.db.models.Model):
    to_team = django.db.models.ForeignKey(
        to=teams.models.Team,
        on_delete=django.db.models.CASCADE,
        verbose_name='команда',
        help_text='в какому команду подан запрос?',
    )
    from_user = django.db.models.ForeignKey(
        to=User,
        on_delete=django.db.models.DO_NOTHING,
        verbose_name='пользователь',
        help_text='кто отправил запрос?',
    )

    class Meta:
        verbose_name = 'запрос на вступление'
        verbose_name_plural = 'запросы на вступление'
        default_related_name = 'request'

    def __str__(self):
        return (
            f'Запрос на вступление от пользователя {self.from_user.username}'
        )
