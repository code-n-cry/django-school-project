import django.db.models

import skills.models


class SkillManager(django.db.models.Manager):
    def ordered(self):
        return (
            self.get_queryset()
            .only(
                skills.models.Skill.name.field.name,
            )
            .order_by(
                f'-{skills.models.Skill.name.field.name}',
            )
        )
