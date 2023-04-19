import django.db.models
import django.urls
import django.views.generic
from django.utils import timezone, translation

import skills.models
import tasks.models
import tasks.utils
import teams.models


class HomeView(django.views.generic.TemplateView):
    template_name = 'homepage/home.html'

    def get(self, request, *args, **kwargs):
        opened_teams = teams.models.Team.objects.opened()
        context = self.get_context_data()
        if request.user.is_authenticated:
            opened_teams = (
                teams.models.Team.objects.opened()
                .exclude(members__in=request.user.teams.all())
                .filter(skills__in=request.user.skills.all())
            )
            lead_teams = (
                teams.models.Team.objects.all()
                .filter(
                    members__in=request.user.teams.all().filter(is_lead=True)
                )
                .prefetch_related(
                    django.db.models.Prefetch(
                        teams.models.Team.skills.field.name,
                        queryset=skills.models.Skill.objects.all(),
                    )
                )
                .order_by(teams.models.Team.name.field.name)
                .only(
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
                .exclude(id__in=lead_teams)
                .filter(members__in=request.user.teams.all())
                .order_by(teams.models.Team.name.field.name)
                .prefetch_related(
                    django.db.models.Prefetch(
                        teams.models.Team.skills.field.name,
                        queryset=skills.models.Skill.objects.all(),
                    )
                )
                .only(
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
            current_date = timezone.now()
            users_meetings = (
                tasks.models.Meeting.objects.all().filter(
                    planned_date__year=current_date.year,
                    planned_date__month=current_date.month,
                    team__members__in=request.user.teams.all(),
                )
            ).values(
                tasks.models.Meeting.id.field.name,
                tasks.models.Meeting.name.field.name,
                tasks.models.Meeting.planned_date.field.name,
            )
            html_calendar = tasks.utils.Calendar(
                request,
                users_meetings,
                translation.get_language() + '.UTF-8',
                current_date.year,
                current_date.month,
            ).formatmonth(with_year=True)
            context.update(
                lead_teams=lead_teams,
                other_teams=other_teams,
                calendar=html_calendar,
            )
        context.update(opened_teams=opened_teams, **kwargs)
        return self.render_to_response(context)
