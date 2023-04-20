from django.views.generic import CreateView, FormView

import skills.forms
import skills.models


class AddSkillView(CreateView):
    model = skills.models.Skill
    form_class = skills.forms.SkillCreationForm
    success_url = '/skills/all'
    template_name = 'skills/create.html'

    def form_invalid(self, form):
        if not form.is_valid():
            form.add_error('name', 'Такой навык уже существует!')
        return super().form_invalid(form)
