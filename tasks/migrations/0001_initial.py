from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='как называется?',
                        max_length=150,
                        verbose_name='название',
                    ),
                ),
                (
                    'detail',
                    models.TextField(
                        blank=True,
                        help_text='более подробное описание',
                        null=True,
                        verbose_name='детали',
                    ),
                ),
                (
                    'planned_date',
                    models.DateTimeField(
                        help_text='когда пройдёт митап?',
                        verbose_name='дата встречи',
                    ),
                ),
                (
                    'status',
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, 'Ожидается'),
                            (1, 'Идёт'),
                            (2, 'Закончилась'),
                        ],
                        default=0,
                        help_text='текущий статус встречи',
                        verbose_name='статус',
                    ),
                ),
            ],
            options={
                'verbose_name': 'встреча',
                'verbose_name_plural': 'встречи',
                'default_related_name': 'meeting',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='как называется?',
                        max_length=150,
                        verbose_name='название',
                    ),
                ),
                (
                    'detail',
                    models.TextField(
                        blank=True,
                        help_text='более подробное описание',
                        null=True,
                        verbose_name='детали',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='когда создана команда?',
                        verbose_name='дата создания',
                    ),
                ),
                (
                    'deadline_date',
                    models.DateTimeField(
                        help_text='до какого времени надо сдать задачу?',
                        verbose_name='дата дедлайна',
                    ),
                ),
                (
                    'completed_date',
                    models.DateTimeField(
                        help_text='когда была выполнена задача?',
                        null=True,
                        verbose_name='дата выполнения',
                    ),
                ),
            ],
            options={
                'verbose_name': 'задача',
                'verbose_name_plural': 'задачи',
                'default_related_name': 'task',
            },
        ),
    ]
