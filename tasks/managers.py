import django.db.models
from django.utils import timezone

import tasks.models


class TasksManager(django.db.models.Manager):
    def failed(self):
        now = timezone.now()
        return (
            self.get_queryset()
            .filter(
                completed_date__isnull=True,
                deadline_date__lte=now,
            )
            .only(
                tasks.models.Task.name.field.name,
                tasks.models.Task.detail.field.name,
                tasks.models.Task.deadline_date.field.name,
            )
        )

    def completed(self):
        now = timezone.now()
        return (
            self.get_queryset()
            .filter(
                completed_date__isnull=False,
                deadline_date__gt=now,
            )
            .only(
                tasks.models.Task.name.field.name,
                tasks.models.Task.detail.field.name,
                tasks.models.Task.completed_date.field.name,
                tasks.models.Task.deadline_date.field.name,
            )
        )

    def uncompleted(self):
        now = timezone.now()
        return (
            self.get_queryset()
            .filter(
                completed_date__isnull=True,
                deadline_date__gt=now,
            )
            .only(
                tasks.models.Task.name.field.name,
                tasks.models.Task.detail.field.name,
                tasks.models.Task.deadline_date.field.name,
            )
        )
