import django.shortcuts
import django.urls
import django.views.generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import tasks.models


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
