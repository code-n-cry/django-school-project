import django.urls
import django.views.generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator

import tasks.forms
import tasks.models
import teams.models


@method_decorator(login_required, name='dispatch')
class TaskCreateView(django.views.generic.FormView):
    template_name = 'tasks/create.html'
    queryset = tasks.models.Task.objects.all()
    form_class = tasks.forms.TaskCreationForm
    http_method_names = ['get', 'post', 'head']
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            teams.models.Team,
            pk=kwargs['team_id'],
            members__user=self.request.user.pk,
            members__is_lead=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        team_id = self.kwargs['team_id']
        kwargs = super().get_form_kwargs()
        kwargs['team_id'] = team_id
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data.copy()
        users = cleaned_data.pop('users')
        task = tasks.models.Task.objects.create(
            **cleaned_data, team_id=self.kwargs['team_id']
        )
        task.users.set(users)
        task.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TaskDoneView(django.views.generic.DetailView):
    http_method_names = ['get']

    def get_queryset(self):
        return tasks.models.Task.objects.filter(
            pk=self.kwargs['pk'], users=self.request.user.pk
        )

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = True
        task.save()
        return redirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class MeetingDetailView(django.views.generic.DetailView):
    model = tasks.models.Meeting
    context_object_name = 'meeting'
    template_name = 'tasks/meeting_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user not in self.object.team.all()[0].members.all():
            return django.shortcuts.redirect(
                django.urls.reverse('homepage:home')
            )
        return super().get(request, *args, **kwargs)
