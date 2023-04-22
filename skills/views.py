from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView

import skills.forms
import skills.models


@method_decorator(login_required, name='dispatch')
class AddSkillView(FormView):
    form_class = skills.forms.SkillCreationForm
    template_name = 'skills/create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', '/'))
        form.add_error('name', _('Похожее название уже существует!'))
        return super().post(request, *args, **kwargs)


class ListSkillView(ListView):
    queryset = skills.models.Skill.objects.ordered()
    template_name = 'skills/list.html'
    paginate_by = 10
    context_object_name = 'skills'
