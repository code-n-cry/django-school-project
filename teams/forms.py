from core.forms import BaseTailwindModelForm
from core.widgets import CheckboxInput
from teams.models import Team
import django.forms
from django.utils.translation import gettext_lazy as _

import teams.models


class TeamCreationForm(BaseTailwindModelForm):
    class Meta:
        model = Team
        exclude = [Team.tasks.field.name]
        widgets = {
            Team.is_open.field.name: CheckboxInput,
        }


class TeamForm(django.forms.ModelForm):
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
