from django.utils.translation import gettext_lazy as _

import core.forms
import skills.models


class SkillCreationForm(core.forms.BaseTailwindModelForm):
    class Meta:
        model = skills.models.Skill
        fields = (skills.models.Skill.name.field.name,)
        labels = {skills.models.Skill.name.field.name: _('Название')}
        help_texts = {
            skills.models.Skill.name.field.name: _(
                'Укажите название навыка(уникальное, не больше 25 символов)'
            )
        }
