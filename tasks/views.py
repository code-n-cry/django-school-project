import zoneinfo
from datetime import datetime

import django.urls
import django.views.generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone, translation
from django.utils.decorators import method_decorator

import tasks.forms
import tasks.models
import teams.models

@method_decorator(login_required, name='dispatch')
class TaskListView(django.views.generic.ListView):
    template_name = 'tasks/your_tasks.html'
    queryset = tasks.models.Task.objects.all()
    context_object_name = 'tasks'
    http_method_names = ['get']

@method_decorator(login_required, name='dispatch')
class TaskCreateView(django.views.generic.FormView):
    template_name = 'tasks/create.html'
    queryset = tasks.models.Task.objects.all()
    form_class = tasks.forms.TaskCreationForm
    http_method_names = ['get', 'post', 'head']
    success_url = '.'

    def dispatch(self, request, *args, **kwargs):
        is_user_lead = teams.models.Team.objects.filter(
            pk=kwargs['team_id'],
            members__user=self.request.user,
            members__is_lead=True,
        ).exists()
        if not is_user_lead:
            return redirect('homepage:home')
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
        task.deadline_date = task.deadline_date.replace(
            tzinfo=zoneinfo.ZoneInfo(self.request.COOKIES['django_timezone'])
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
        task.completed_date = datetime.now()
        task.save()
        return redirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class MeetingDetailView(django.views.generic.DetailView):
    model = tasks.models.Meeting
    context_object_name = 'meeting'
    template_name = 'tasks/meeting_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_user_member = self.object.team.members.filter(
            user=request.user
        ).exists()
        if not is_user_member:
            return django.shortcuts.redirect(
                django.urls.reverse('homepage:home')
            )
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class YourMeetingsView(django.views.generic.TemplateView):
    template_name = 'tasks/your_meetings.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
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
            calendar=html_calendar,
        )
        return self.render_to_response(context, **kwargs)
