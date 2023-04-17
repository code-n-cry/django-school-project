import django.contrib.auth.forms
import django.forms
import django.utils.html
from django.conf import settings
from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy

import teams.models
from core.forms import BaseTailwindForm, BaseTailwindModelForm
from core.widgets import CheckboxInput, ImageInput
from users.models import Invite, User


class AuthenticationForm(BaseTailwindForm, forms.AuthenticationForm):
    ...


class PasswordChangeForm(BaseTailwindForm, forms.PasswordChangeForm):
    ...


class PasswordResetForm(BaseTailwindForm, forms.PasswordResetForm):
    ...


class SetPasswordForm(BaseTailwindForm, forms.SetPasswordForm):
    ...


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
            user_with_same_email = User.objects.filter(
                ~Q(pk=self.instance.pk), email=self.cleaned_data['email']
            ).exists()
            if user_with_same_email:
                raise ValidationError(
                    gettext_lazy(
                        'Пользователь с такой почтой уже зарегистрирован!'
                    )
                )
            return User.objects.normalize_email(self.cleaned_data['email'])
        raise ValidationError(
            gettext_lazy('Введите новый email или оставьте старый!')
        )


class SignUpForm(
    BaseTailwindModelForm, django.contrib.auth.forms.UserCreationForm
):
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


class InviteForm(BaseTailwindModelForm):
    class Meta:
        model = Invite
        fields = (Invite.to_user.field.name,)


class RequestForm(BaseTailwindForm):
    to_team = django.forms.ModelChoiceField(
        queryset=teams.models.Team.objects.opened().only(
            teams.models.Team.id.field.name,
            teams.models.Team.name.field.name,
        ),
        label=gettext_lazy('В команду:'),
        help_text=gettext_lazy('В какую команду запрос?'),
    )
