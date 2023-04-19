import django.forms
from django.utils.translation import gettext_lazy as _

import skills.models


class SkillCreationForm(django.forms.ModelForm):
    class Meta:
        model = skills.models.Skill
        fields = (skills.models.Skill.name.field.name,)
        labels = {skills.models.Skill.name.field.name: _('Название')}
        help_texts = {
            skills.models.Skill.name.field.name: _(
                'Укажите название навыка(уникальное, не больше 25 символов)'
            )
        }
