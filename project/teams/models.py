import django.db.models
import sorl
from django.templatetags.static import static
from django.utils import timezone

import core.models
import skills.models
import teams.managers


def avatar_image_path(instance, filename):
    return ''.join(
        [
            f'uploads/teams/{instance.id}-',
            timezone.now().strftime('%Y-%d-%m-%H%M%S'),
            f'/{filename}',
        ]
    )


class Team(core.models.UniqueNameWithDetailAbstractModel):
    objects = teams.managers.TeamManager()

    created_at = django.db.models.DateTimeField(
        verbose_name='дата создания',
        help_text='когда создана команда?',
        auto_now_add=True,
    )
    is_open = django.db.models.BooleanField(
        default=True,
        verbose_name='открытость',
        help_text='показывается ли ваша команда в поиске?',
    )
    skills = django.db.models.ManyToManyField(
        to=skills.models.Skill,
        verbose_name='требуемые навыки',
        help_text='какие навыки нужны команде?',
    )
    avatar = django.db.models.ImageField(
        upload_to=avatar_image_path,
        verbose_name='аватарка',
        help_text='картинка профиля команды',
        blank=True,
    )

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'
        default_related_name = 'team'

    def __str__(self):
        return self.name

    def get_avatar_300x300(self):
        if self.avatar:
            return sorl.thumbnail.get_thumbnail(
                self.avatar, '300x300', crop='center', quality=65
            )
        return {'url': static('img/team_default.png')}
