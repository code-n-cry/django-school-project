from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from users.models import Comment, Invite, Member, User


class MemberInline(admin.TabularInline):
    model = Member


class CustomUserAdminForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(Comment)
class ReportedCommentAdmin(admin.ModelAdmin):
    fields = (Comment.content.field.name, Comment.is_reported.field.name)
    readonly_fields = (Comment.content.field.name,)

    def get_queryset(self, request):
        return Comment.objects.filter(is_reported=True).only(
            Comment.id.field.name,
            Comment.content.field.name,
            Comment.is_reported.field.name,
        )


class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                'fields': (
                    User.avatar.field.name,
                    User.skills.field.name,
                )
            },
        ),
    )
    inlines = (MemberInline,)


admin.site.register(User, CustomUserAdmin)


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass
