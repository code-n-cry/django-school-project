import django.urls
import django.views.generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import teams.forms
import teams.models


@method_decorator(login_required, name='dispatch')
class CreateTeamView(django.views.generic.FormView):
    template_name = 'teams/create.html'
    form_class = teams.forms.TeamCreationForm
    success_url = django.urls.reverse_lazy('homepage:home')

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


class TeamListView(django.views.generic.ListView):
    template_name = 'teams/list.html'
    queryset = teams.models.Team.objects.opened()
    context_object_name = 'teams'
    http_method_names = ['get', 'head']
