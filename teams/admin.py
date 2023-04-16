from django.contrib import admin

import teams.models
import users.models


class MembersInlineAdmin(admin.TabularInline):
    model = users.models.Member


@admin.register(teams.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        teams.models.Team.name.field.name,
        teams.models.Team.is_open.field.name,
    )
    list_display_links = (teams.models.Team.name.field.name,)
    list_editable = (teams.models.Team.is_open.field.name,)
    inlines = (MembersInlineAdmin,)
