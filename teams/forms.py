from core.forms import BaseTailwindModelForm
from core.widgets import CheckboxInput
from teams.models import Team


class TeamCreationForm(BaseTailwindModelForm):
    class Meta:
        model = Team
        exclude = [Team.tasks.field.name]
        widgets = {
            Team.is_open.field.name: CheckboxInput,
        }
