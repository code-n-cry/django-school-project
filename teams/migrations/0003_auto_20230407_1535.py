# Generated by Django 3.2.17 on 2023-04-07 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_squashed_0002_auto_20230406_2110'),
        ('teams', '0002_auto_20230407_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='meetings',
            field=models.ForeignKey(
                blank=True,
                help_text='запланированные командные встречи',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='team',
                to='tasks.meeting',
                verbose_name='встречи',
            ),
        ),
        migrations.AlterField(
            model_name='team',
            name='tasks',
            field=models.ForeignKey(
                blank=True,
                help_text='задания для команды',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='team',
                to='tasks.task',
                verbose_name='задания',
            ),
        ),
    ]
