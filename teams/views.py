from django.views.generic import FormView

from teams.forms import TeamCreationForm


class CreateTeamView(FormView):
    template_name = 'teams/create.html'
    form_class = TeamCreationForm
