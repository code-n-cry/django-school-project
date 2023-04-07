from django.contrib import admin
from django.contrib.auth import get_user_model

import teams.models


class LeadsInlineAdmin(admin.TabularInline):
    model = get_user_model().lead_teams.through


class MembersInlineAdmin(admin.TabularInline):
    model = get_user_model().teams.through


@admin.register(teams.models.Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = (
        LeadsInlineAdmin,
        MembersInlineAdmin,
    )
