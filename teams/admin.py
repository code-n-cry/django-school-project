from django.contrib import admin
from django.contrib.auth import get_user_model

import teams.models


class LeadsInlineAdmin(admin.TabularInline):
    model = get_user_model().lead_teams.through


class MembersInlineAdmin(admin.TabularInline):
    model = get_user_model().teams.through


@admin.register(teams.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        teams.models.Team.name.field.name,
        teams.models.Team.is_open.field.name,
    )
    list_display_links = (teams.models.Team.name.field.name,)
    list_editable = (teams.models.Team.is_open.field.name,)
    inlines = (
        LeadsInlineAdmin,
        MembersInlineAdmin,
    )
