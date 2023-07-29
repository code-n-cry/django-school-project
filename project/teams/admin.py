from django.contrib import admin

import tasks.models
import teams.models
import users.models


class MembersInlineAdmin(admin.TabularInline):
    model = users.models.Member


class TasksInlineAdmin(admin.TabularInline):
    model = tasks.models.Task


class MeetingsInlineAdmin(admin.TabularInline):
    model = tasks.models.Meeting


@admin.register(teams.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        teams.models.Team.name.field.name,
        teams.models.Team.is_open.field.name,
    )
    list_display_links = (teams.models.Team.name.field.name,)
    list_editable = (teams.models.Team.is_open.field.name,)
    inlines = (
        MembersInlineAdmin,
        TasksInlineAdmin,
        MeetingsInlineAdmin,
    )
