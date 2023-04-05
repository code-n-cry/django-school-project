from django.contrib import admin

import teams.models


@admin.register(teams.models.Team)
class TeamAdmin(admin.ModelAdmin):
    pass
