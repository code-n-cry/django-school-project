import django.db.models

import skills.models
import teams.models


class TeamManager(django.db.models.Manager):
    def opened(self):
        return (
            self.get_queryset()
            .filter(is_open=True)
            .prefetch_related(
                django.db.models.Prefetch(
                    teams.models.Team.skills.field.name,
                    queryset=skills.models.Skill.objects.all(),
                )
            )
            .only(
                teams.models.Team.name.field.name,
                teams.models.Team.detail.field.name,
                teams.models.Team.created_at.field.name,
                teams.models.Team.avatar.field.name,
            )
            .order_by(
                teams.models.Team.name.field.name,
            )
        )
