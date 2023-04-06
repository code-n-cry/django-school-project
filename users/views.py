import datetime

import django.core.mail
import django.urls
import django.utils.timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views import View
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

import users.forms
import users.models


class ActivateNewView(View):
    http_method_names = ['get', 'head']

    def get(self, request, username, *args, **kwargs):
        user = users.models.User.objects.filter(
            username=username,
            date_joined__range=[
                django.utils.timezone.now() - datetime.timedelta(hours=12),
                django.utils.timezone.now(),
            ],
        ).first()
        if not user:
            messages.error(
                request,
                gettext_lazy(
                    'Прошло больше 12 часов, ссылка уже не работает:('
                ),
            )
            return redirect('homepage:index')
        user.is_active = True
        user.save()
        messages.success(request, gettext_lazy('Вы активированы!'))
        return redirect('homepage:index')


class ActivateView(View):
    http_method_names = ['get', 'head']

    def get(self, request, username, *args, **kwargs):
        user = users.models.User.objects.filter(
            username=username,
            profile__last_failed_login_date__range=[
                django.utils.timezone.now() - datetime.timedelta(weeks=1),
                django.utils.timezone.now(),
            ],
        ).first()
        if not user:
            messages.error(
                request,
                gettext_lazy('Прошла неделя, ссылка уже не работает:('),
            )
            return redirect('homepage:index')
        user.is_active = True
        user.save()
        messages.success(request, 'Аккаунт восстановлен')
        return redirect('auth:login')


class SignUpView(FormView):
    form_class = users.forms.SignUpForm
    model = users.models.User
    success_url = django.urls.reverse_lazy('auth:login')
    template_name = None
    http_method_names = ['get', 'head', 'post']

    def form_valid(self, form):
        email_text = ''.join(
            [
                'Ваша ссылка для активации: ',
                self.request.build_absolute_uri(
                    django.urls.reverse(
                        'auth:activate_new',
                        kwargs={'username': form.cleaned_data['username']},
                    )
                ),
            ]
        )
        form.save()
        django.core.mail.send_mail(
            gettext_lazy('Активация'),
            email_text,
            settings.EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, gettext_lazy('Вы уже авторизованы!'))
            return redirect('homepage:index')
        return self.render_to_response(self.get_context_data(**kwargs))


class UserListView(ListView):
    template_name = None
    queryset = users.models.User.objects.public()
    context_object_name = 'users'
    http_method_names = ['get', 'head']


class UserDetailView(DetailView):
    template_name = None
    queryset = users.models.User.objects.public()
    context_object_name = 'user'
    http_method_names = ['get', 'head']


class UnauthorizedView(TemplateView):
    template_name = None
    http_method_names = ['get', 'head']


@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    template_name = None
    model = users.models.User
    form_class = users.forms.ProfileForm
    http_method_names = ['get', 'head', 'post']