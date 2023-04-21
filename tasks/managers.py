import django.db.models
from django.utils import timezone

import tasks.models
import teams.models


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
        return (
            self.get_queryset()
            .filter(
                completed_date__isnull=True,
            )
            .only(
                tasks.models.Task.name.field.name,
                tasks.models.Task.detail.field.name,
                tasks.models.Task.deadline_date.field.name,
            )
        )


class MeetingManager(django.db.models.Manager):
    def today(self):
        now = timezone.now()
        return (
            self.get_queryset()
            .filter(
                planned_date__year=now.year,
                planned_date__month=now.month,
                planned_date__day=now.day,
            )
            .select_related(tasks.models.Meeting.team.field.name)
            .only(
                '__'.join(
                    [
                        tasks.models.Meeting.team.field.name,
                        teams.models.Team.members.field.name,
                    ]
                ),
                tasks.models.Meeting.name.field.name,
                tasks.models.Meeting.planned_date.field.name,
            )
            .order_by(f'-{tasks.models.Meeting.name.field.name}')
        )
