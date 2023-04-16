import django.urls
import django.views.generic

import teams.forms
import teams.models
import users.models


class CreateTeamView(django.views.generic.FormView):
    template_name = 'teams/create.html'
    form_class = teams.forms.TeamCreationForm
    success_url = django.urls.reverse_lazy('homepage:index')

    def form_valid(self, form):
        team = form.save()
        member = users.models.Member.objects.create(
            is_lead=True, team=team, user=self.request.user
        )
        member.save()
        return super().form_valid(form)


class TeamDetailView(django.views.generic.DetailView):
    template_name = 'teams/detail.html'
    queryset = teams.models.Team.objects.all()
    context_object_name = 'team'
    http_method_names = ['get', 'head']


class TeamListView(django.views.generic.ListView):
    template_name = 'teams/list.html'
    queryset = teams.models.Team.objects.all()
    context_object_name = 'teams'
    http_method_names = ['get', 'head']


class UsersTeamListView(django.views.generic.ListView):
    template_name = 'teams/list.html'
    queryset = teams.models.Team.objects.all()
    context_object_name = 'teams'
    http_method_names = ['get', 'head']

    def get_queryset(self):
        field_is_lead = '__'.join(
            [
                teams.models.Team.members.rel.related_name,
                users.models.Member.is_lead.field.name,
            ]
        )
        return (
            super()
            .get_queryset()
            .filter(members__user=self.request.user)
            .order_by(f'-{field_is_lead}')
        )
