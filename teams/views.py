import django.views.generic

import teams.forms
import teams.models


class CreateTeamView(django.views.generic.FormView):
    template_name = 'teams/create.html'
    form_class = teams.forms.TeamCreationForm

    def form_valid(self, form):
        team = form.save()
        self.request.user.teams.add(team.pk)
        self.request.user.lead_teams.add(team.pk)
        return super().form_valid(form)


class TeamDetailView(django.views.generic.DetailView):
    template_name = 'teams/detail.html'
    queryset = teams.models.Team.objects.all()
    context_object_name = 'team'
    http_method_names = ['get', 'head']
