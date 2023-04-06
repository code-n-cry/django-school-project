import django.db.models
import django.utils.html
import sorl
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy

import teams.models
import users.managers


def avatar_image_path(instance, filename):
    return f'uploads/{instance.id}-{timezone.now}/{filename}'


class User(AbstractUser):
    objects = users.managers.ActiveUserManager()

    is_visible = django.db.models.BooleanField(
        default=True,
        verbose_name='статус видимости',
        help_text='могут ли другие пользователи звать вас в команды?',
    )
    lead_teams = django.db.models.ManyToManyField(
        teams.models.Team,
        verbose_name='управляемые команды',
        help_text='какими командами вы управляете?',
        related_name='leads',
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
        null=True,
    )
    avatar = django.db.models.ImageField(
        upload_to=avatar_image_path,
        verbose_name='аватарка',
        help_text='картинка профиля пользователя',
        null=True,
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
        return sorl.thumbnail.get_thumbnail(
            self.avatar, '300x300', crop='center', quality=65
        )

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
