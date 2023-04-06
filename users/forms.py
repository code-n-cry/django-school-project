import django.contrib.auth.forms
import django.forms
import django.utils.html
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy

from users.models import User


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


class ProfileForm:
    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.avatar.field.name,
            User.is_visible.field.name,
        )
        labels = {
            User.username.field.name: gettext_lazy('Юзернейм'),
            User.email.field.name: 'E-mail',
            User.first_name.field.name: gettext_lazy('Имя(если хотите)'),
            User.last_name.field.name: gettext_lazy('Фамилия(если хотите)'),
            User.avatar.field.name: gettext_lazy('Аватарка'),
            User.is_visible.field.name: gettext_lazy('Ваша публичность'),
        }
        help_texts = {
            User.username.field.name: gettext_lazy('Измените имя'),
            User.email.field.name: gettext_lazy('Измените почту'),
            User.first_name.field.name: gettext_lazy('Измените имя'),
            User.last_name.field.name: gettext_lazy('Измените фамилию'),
            User.avatar.field.name: gettext_lazy('Загрузите фото профиля'),
            User.is_visible.field.name: gettext_lazy(
                'Будут ли другие пользователи видеть Вас и Вашу статистику'
            ),
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
        user = User.objects.create_user(
            cleaned_data['username'],
            cleaned_data['email'],
            cleaned_data['password1'],
            is_active=settings.USER_ACTIVE_DEFAULT,
        )
        return user

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
