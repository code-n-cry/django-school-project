import django.db.models


class Task(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name='название задачи',
        help_text='как будет называться задача?',
        max_length=150,
        unique=True,
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='дата создания',
        help_text='когда создана команда?',
        auto_now_add=True,
    )
    deadline_date = django.db.models.DateTimeField(
        verbose_name='дата дедлайна',
        help_text='до какого времени надо сдать задачу?',
    )
    completed_date = django.db.models.DateTimeField(
        verbose_name='дата выполнения',
        help_text='когда была выполнена задача?',
        null=True,
    )

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        default_related_name = 'task'
