from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from users.models import Invite, User


class CustomUserAdminForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                'fields': (
                    User.avatar.field.name,
                    User.lead_teams.field.name,
                    User.teams.field.name,
                    User.skills.field.name,
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass
