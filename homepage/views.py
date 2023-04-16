import django.db.models
import django.urls
import django.views.generic

import skills.models
import teams.models


class HomeView(django.views.generic.TemplateView):
    template_name = 'homepage/home.html'

    def get(self, request, *args, **kwargs):
        opened_teams = teams.models.Team.objects.opened()
        context = self.get_context_data()
        if request.user.is_authenticated:
            opened_teams = (
                teams.models.Team.objects.opened()
                .exclude(id__in=request.user.teams.all())
                .filter(skills__id__in=request.user.skills.all())
            )
            lead_teams = (
                teams.models.Team.objects.all()
                .filter(id__in=request.user.lead_teams.all())
                .prefetch_related(
                    django.db.models.Prefetch(
                        teams.models.Team.skills.field.name,
                        queryset=skills.models.Skill.objects.all(),
                    )
                )
                .order_by(teams.models.Team.name.field.name)
                .values(
                    teams.models.Team.id.field.name,
                    teams.models.Team.avatar.field.name,
                    teams.models.Team.name.field.name,
                    '__'.join(
                        [
                            teams.models.Team.skills.field.name,
                            skills.models.Skill.name.field.name,
                        ]
                    ),
                )
            )
            other_teams = (
                teams.models.Team.objects.all()
                .exclude(id__in=request.user.lead_teams.all())
                .filter(id__in=request.user.teams.all())
                .order_by(teams.models.Team.name.field.name)
                .prefetch_related(
                    django.db.models.Prefetch(
                        teams.models.Team.skills.field.name,
                        queryset=skills.models.Skill.objects.all(),
                    )
                )
                .values(
                    teams.models.Team.id.field.name,
                    teams.models.Team.avatar.field.name,
                    teams.models.Team.name.field.name,
                    '__'.join(
                        [
                            teams.models.Team.skills.field.name,
                            skills.models.Skill.name.field.name,
                        ]
                    ),
                )
            )
            context.update(lead_teams=lead_teams, other_teams=other_teams)
        context.update(opened_teams=opened_teams, **kwargs)
        return self.render_to_response(context)
