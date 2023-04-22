from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import core.forms
import teams.models
import users.models
from core.widgets import CheckboxInput, ImageInput
from teams.models import Team


class TeamForm(core.forms.BaseTailwindModelForm):
    class Meta:
        model = teams.models.Team
        fields = (
            teams.models.Team.name.field.name,
            teams.models.Team.detail.field.name,
            teams.models.Team.is_open.field.name,
            teams.models.Team.avatar.field.name,
            teams.models.Team.skills.field.name,
        )
        labels = {
            teams.models.Team.name.field.name: _('Название'),
            teams.models.Team.detail.field.name: _('Описание'),
            teams.models.Team.is_open.field.name: _('Открытая?'),
            teams.models.Team.avatar.field.name: _('Аватарка'),
            teams.models.Team.skills.field.name: _('Навыки(тэги)'),
        }
        help_texts = {
            teams.models.Team.name.field.name: _(
                'Как будет называться команда?'
            ),
            teams.models.Team.detail.field.name: _(
                'Расскажите о команде подробнее.'
            ),
            teams.models.Team.is_open.field.name: _(
                'Будет ли показываться команда всем пользователям?'
            ),
            teams.models.Team.avatar.field.name: _(
                'Профильное изображение команды'
            ),
            teams.models.Team.skills.field.name: _(
                'Что должен уметь участник команды?'
            ),
        }
        widgets = {
            Team.avatar.field.name: ImageInput,
            Team.is_open.field.name: CheckboxInput,
        }


class TeamInviteUserForm(core.forms.BaseTailwindModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            users.models.Invite.to_user.field.name
        ].queryset = get_user_model().objects.exclude(pk=request.user.pk)

    class Meta:
        model = users.models.Invite
        fields = (users.models.Invite.to_user.field.name,)
