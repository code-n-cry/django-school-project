import django.shortcuts
import django.urls
import django.views.generic
import django.db.models
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
    form_class = teams.forms.TeamForm
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
    form_class = teams.forms.TeamForm
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
        context['meeting_form'] = self.meeting_form_class()
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
            meeting = meeting_form.save(commit=False)
            meeting.team = self.object
            meeting.save()
        return self.render_to_response(context)


class TeamDetailView(django.views.generic.DetailView):
    template_name = 'teams/detail.html'
    queryset = teams.models.Team.objects.all()
    context_object_name = 'team'
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset.filter(is_open=True)
        if self.request.user.is_authenticated:
            result = queryset.filter(members__user=self.request.user)
        return result.prefetch_related(
            django.db.models.Prefetch(
                teams.models.Team.members.rel.related_name,
                queryset=users.models.Member.objects.all(),
            ),
            django.db.models.Prefetch(
                '__'.join(
                    [
                        teams.models.Team.members.rel.related_name,
                        users.models.Member.user.field.name,
                    ]
                )
            ),
        )

    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
        except django.http.Http404:
            obj = self.queryset.none()
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        member = None
        if self.object and request.user.is_authenticated:
            member = self.object.members.filter(user=request.user).first()
        context = self.get_context_data(object=self.object, member=member)
        return self.render_to_response(context)


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
        is_request_user_lead = (
            teams.models.Team.objects.all()
            .filter(members__user=self.request.user, members__is_lead=True)
            .exists()
        )
        if not team or not is_request_user_lead:
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


@method_decorator(login_required, name='dispatch')
class RequestAcceptView(django.views.generic.View):
    http_method_names = ['get', 'head']

    def get(self, *args, **kwargs):
        team = get_object_or_404(
            teams.models.Team.objects.opened(), pk=kwargs['team_id']
        )
        is_request_user_lead = (
            teams.models.Team.objects.all()
            .filter(members__user=self.request.user, members__is_lead=True)
            .exists()
        )
        if is_request_user_lead:
            request = get_object_or_404(
                users.models.Request, pk=kwargs['request_id'], to_team=team
            )
            users.models.Member.objects.create(
                user=request.from_user, team=team
            )
            request.delete()
            return redirect(
                django.urls.reverse(
                    'teams:requests', kwargs={'pk': kwargs['team_id']}
                )
            )
        return redirect('homepage:home')


@method_decorator(login_required, name='dispatch')
class RequestRejectView(django.views.generic.View):
    http_method_names = ['get', 'head']

    def get(self, *args, **kwargs):
        team = get_object_or_404(
            teams.models.Team.objects.opened(), pk=kwargs['team_id']
        )
        is_request_user_lead = (
            teams.models.Team.objects.all()
            .filter(members__user=self.request.user, members__is_lead=True)
            .exists()
        )
        if is_request_user_lead:
            request = get_object_or_404(
                users.models.Request, pk=kwargs['request_id'], to_team=team
            )
            request.delete()
            return redirect(
                django.urls.reverse(
                    'teams:requests', kwargs={'pk': kwargs['team_id']}
                )
            )
        return redirect('homepage:home')
