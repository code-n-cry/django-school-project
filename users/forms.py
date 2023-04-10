import django.contrib.auth.forms
import django.forms
import django.utils.html
from django.conf import settings
from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy

from core.forms import BaseTailwindForm, BaseTailwindModelForm
from core.widgets import CheckboxInput, ImageInput
from users.models import Invite, Request, User


class AuthenticationForm(BaseTailwindForm, forms.AuthenticationForm):
    ...


class PasswordChangeForm(BaseTailwindForm, forms.PasswordChangeForm):
    ...


class PasswordResetForm(BaseTailwindForm, forms.PasswordResetForm):
    ...


class SetPasswordForm(BaseTailwindForm, forms.SetPasswordForm):
    ...


class UserCreationForm(BaseTailwindForm, forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = (
            User.username.field.name,
            User.avatar.field.name,
        )
        widgets = {User.avatar.field.name: ImageInput}


class StyledLoginForm(django.contrib.auth.forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StyledResetPasswordForm(django.contrib.auth.forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StyledChangePasswordForm(django.contrib.auth.forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StyledSetPassword(django.contrib.auth.forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProfileForm(BaseTailwindModelForm):
    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
            User.is_visible.field.name,
            User.avatar.field.name,
        )
        widgets = {
            User.avatar.field.name: ImageInput,
            User.is_visible.field.name: CheckboxInput,
        }

    def clean_email(self):
        if self.cleaned_data['email']:
            is_email_unique = User.objects.filter(
                ~Q(pk=self.instance.id), email=self.cleaned_data['email']
            ).exists()
            if is_email_unique:
                raise ValidationError(
                    gettext_lazy(
                        'Пользователь с такой почтой уже зарегистрирован!'
                    )
                )
            return User.objects.normalize_email(self.cleaned_data['email'])
        raise ValidationError(
            gettext_lazy('Введите новый email или оставьте старый!')
        )


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        if not self.cleaned_data['email']:
            return self.add_error(
                User.email.field.name, gettext_lazy('Укажите email!')
            )
        normalized_email = User.objects.normalize_email(
            self.cleaned_data['email']
        )
        is_email_unique = User.objects.filter(email=normalized_email).exists()
        if is_email_unique:
            return self.add_error(
                User.email.field.name,
                gettext_lazy(
                    'Пользователь с такой почтой уже зарегистрирован!'
                ),
            )
        return normalized_email

    def save(self, commit: bool = True):
        cleaned_data = super().clean()
        return User.objects.create_user(
            cleaned_data['username'],
            cleaned_data['email'],
            cleaned_data['password1'],
            is_active=settings.USER_ACTIVE_DEFAULT,
        )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
        )
        labels = {
            User.username.field.name: gettext_lazy('Юзернейм'),
            User.email.field.name: 'E-mail',
            User.password.field.name: gettext_lazy('Пароль'),
        }
        help_texts = {
            User.email.field.name: gettext_lazy('Обязательное поле.'),
        }


class InviteForm(django.forms.ModelForm):
    class Meta:
        model = Invite
        fields = (Invite.to_user.field.name,)


class RequestForm(django.forms.ModelForm):
    class Meta:
        model = Request
        fields = (Request.to_team.field.name,)
