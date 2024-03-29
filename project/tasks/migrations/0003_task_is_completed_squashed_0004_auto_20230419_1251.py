# Generated by Django 3.2.17 on 2023-04-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ('tasks', '0003_task_is_completed'),
        ('tasks', '0004_auto_20230419_1251'),
    ]

    dependencies = [
        (
            'tasks',
            '0002_auto_20230418_1935_squashed_0003_alter_task_deadline_date',
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_date',
            field=models.DateTimeField(
                blank=True,
                help_text='когда была выполнена задача?',
                null=True,
                verbose_name='дата выполнения',
            ),
        ),
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(
                default=False, verbose_name='задание выполнено'
            ),
        ),
    ]
