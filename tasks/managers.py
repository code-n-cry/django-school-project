import django.db.models
from django.contrib.auth import get_user_model
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
            .prefetch_related(
                django.db.models.Prefetch(
                    tasks.models.Task.to_users.field.name,
                    queryset=get_user_model().objects.active(),
                )
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
            .prefetch_related(
                django.db.models.Prefetch(
                    tasks.models.Task.to_users.field.name,
                    queryset=get_user_model().objects.active(),
                )
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
            .prefetch_related(
                django.db.models.Prefetch(
                    tasks.models.Task.to_users.field.name,
                    queryset=get_user_model().objects.active(),
                )
            )
            .only(
                tasks.models.Task.name.field.name,
                tasks.models.Task.detail.field.name,
                tasks.models.Task.created_at.field.name,
                tasks.models.Task.deadline_date.field.name,
            )
        )
