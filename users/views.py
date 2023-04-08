from django.contrib.auth import views
from django.views.generic import FormView, TemplateView

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


class ProfileView(FormView):
    template_name = 'users/profile.html'
    form_class = forms.ProfileForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        extra_context = {'form': form}
        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return self.render_to_response(context)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
