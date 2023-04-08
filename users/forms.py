from django.contrib.auth import forms, get_user_model

from core.forms import BaseTailwindForm, BaseTailwindModelForm
from core.widgets import CheckboxInput, ImageInput

UserModel = get_user_model()


class AuthenticationForm(BaseTailwindForm, forms.AuthenticationForm):
    ...


class PasswordChangeForm(BaseTailwindForm, forms.PasswordChangeForm):
    ...


class UserCreationForm(BaseTailwindForm, forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = UserModel
        fields = (
            UserModel.username.field.name,
            UserModel.avatar.field.name,
        )
        widgets = {UserModel.avatar.field.name: ImageInput}


class ProfileForm(BaseTailwindModelForm):
    class Meta:
        model = UserModel
        fields = (
            UserModel.username.field.name,
            UserModel.first_name.field.name,
            UserModel.last_name.field.name,
            UserModel.email.field.name,
            UserModel.is_visible.field.name,
            UserModel.avatar.field.name,
        )
        widgets = {
            UserModel.avatar.field.name: ImageInput,
            UserModel.is_visible.field.name: CheckboxInput,
        }


class PasswordResetForm(BaseTailwindForm, forms.PasswordResetForm):
    ...


class SetPasswordForm(BaseTailwindForm, forms.SetPasswordForm):
    ...
