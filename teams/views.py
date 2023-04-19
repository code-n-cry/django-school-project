import django.shortcuts
import django.urls
import django.views.generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator

import tasks.forms
import tasks.models
import teams.forms
import teams.models
import users.models


@method_decorator(login_required, name='dispatch')
class CreateTeamView(django.views.generic.FormView):
    template_name = 'teams/create.html'
    form_class = teams.forms.TeamCreationForm
    success_url = django.urls.reverse_lazy('homepage:home')
    http_method_names = ['get', 'head', 'post']

    def form_valid(self, form):
        team = form.save()
        member = users.models.Member.objects.create(
            is_lead=True, team=team, user=self.request.user
        )
        member.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TeamEditView(django.views.generic.UpdateView):
    model = teams.models.Team
    template_name = 'teams/edit.html'
    form_class = teams.forms.TeamCreationForm
    meeting_form_class = tasks.forms.MeetingCreationForm
    task_form_class = None
    context_object_name = 'team'
    http_method_names = ['get', 'head', 'post']

    def get_success_url(self):
        return django.urls.reverse(
            'teams:detail', kwargs={'pk': self.object.pk}
        )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        context['meeting_form'] = tasks.forms.MeetingCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(
            request.POST, request.FILES, instance=self.object
        )
        meeting_form = self.meeting_form_class(request.POST)
        context = self.get_context_data()
        if form.is_valid():
            form.save()
        if meeting_form.is_valid():
            meeting = meeting_form.save()
            self.object.meetings.add(meeting)
            self.object.save()
        return self.render_to_response(context)


class TeamDetailView(django.views.generic.DetailView):
    template_name = 'teams/detail.html'
    queryset = teams.models.Team.objects.all().prefetch_related(
        'members__user'
    )
    context_object_name = 'team'
    http_method_names = ['get', 'head']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object
        if self.request.user.is_authenticated:
            if self.request.user.pk in [
                member.user_id for member in team.members.all()
            ]:
                user_tasks = tasks.models.Task.objects.filter(
                    users=self.request.user.pk, team=team
                ).only('name', 'detail', 'is_completed')
                context['all_tasks_count'] = len(user_tasks)
                context['done_tasks_count'] = len(
                    [task for task in user_tasks if not task.is_completed]
                )
                context['tasks'] = [
                    task for task in user_tasks if task.is_completed
                ]
            if self.request.user.pk in [
                member.user_id
                for member in team.members.all()
                if member.is_lead
            ]:
                context['is_lead'] = True
        return context


class TeamListView(django.views.generic.ListView):
    template_name = 'teams/list.html'
    queryset = teams.models.Team.objects.opened()
    context_object_name = 'teams'
    http_method_names = ['get', 'head']


@method_decorator(login_required, name='dispatch')
class TeamRequestsView(django.views.generic.TemplateView):
    template_name = 'teams/all_requests.html'
    model = users.models.Request
    http_method_names = ['get', 'head']

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(teams.models.Team, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        team = (
            teams.models.Team.objects.opened()
            .filter(pk=self.kwargs['pk'])
            .first()
        )
        if not team or request.user not in team.leads.all():
            return redirect(django.urls.reverse('homepage:home'))
        team_requests = (
            users.models.Request.objects.all()
            .filter(to_team=team)
            .select_related(users.models.Request.from_user.field.name)
            .only(
                users.models.Request.id.field.name,
                '__'.join(
                    [
                        users.models.Request.from_user.field.name,
                        users.models.User.id.field.name,
                    ]
                ),
                '__'.join(
                    [
                        users.models.Request.from_user.field.name,
                        users.models.User.username.field.name,
                    ]
                ),
            )
        )
        context = self.get_context_data(**kwargs)
        context.update(requests=team_requests)
        return self.render_to_response(context)
