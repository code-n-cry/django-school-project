from django.contrib import admin

import tasks.models


@admin.register(tasks.models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass
