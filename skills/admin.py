from django.contrib import admin

import skills.models


@admin.register(skills.models.Skill)
class SkillAdmin(admin.ModelAdmin):
    pass
