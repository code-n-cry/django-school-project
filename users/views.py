import datetime

import django.core.mail
import django.urls
import django.utils.timezone
import django.views.generic
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

import users.forms
import users.models
from users import forms


class LoginView(views.LoginView):
    template_name = 'users/login.html'
    form_class = forms.AuthenticationForm


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = forms.PasswordChangeForm


class PasswordChangeDoneView(TemplateView):
    template_name = 'users/password_change_done.html'


class PasswordResetView(views.PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = forms.PasswordResetForm


class PasswordResetDoneView(TemplateView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'users/password_confirm.html'
    form_class = forms.SetPasswordForm


class PasswordResetCompleteView(TemplateView):
    template_name = 'users/password_confirm_done.html'


class SignupView(FormView):
    template_name = 'users/signup.html'
    form_class = forms.UserCreationForm


@method_decorator(login_required, name='dispatch')
class ProfileView(FormView):
    template_name = 'users/profile.html'
    form_class = forms.ProfileForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# << develop, пока под вопросом
# @method_decorator(login_required, name='dispatch')
# class ProfileView(django.views.generic.UpdateView):
#     template_name = None
#     model = users.models.User
#     form_class = users.forms.ProfileForm
#     http_method_names = ['get', 'head', 'post']

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(
#             request.POST, request.FILES, instance=request.user
#         )
#         if form.is_valid():
#             if request.FILES:
#                 request.user.avatar = request.FILES['avatar']
#             form.save()
#         extra_context = {'form': form}
#         context = self.get_context_data(**kwargs)
#         context.update(extra_context)
#         return self.render_to_response(context)


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


class SignUpView(django.views.generic.FormView):
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


class UserListView(django.views.generic.ListView):
    template_name = None
    queryset = users.models.User.objects.public()
    context_object_name = 'users'
    http_method_names = ['get', 'head']


class UserDetailView(django.views.generic.DetailView):
    template_name = 'users/detail.html'
    queryset = users.models.User.objects.public()
    context_object_name = 'user'
    http_method_names = ['get', 'head']


class UnauthorizedView(django.views.generic.TemplateView):
    template_name = None
    http_method_names = ['get', 'head']
