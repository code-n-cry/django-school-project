# Generated by Django 3.2.17 on 2023-04-06 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20230406_2110'),
        ('teams', '0002_auto_20230406_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='meetings',
            field=models.ForeignKey(help_text='запланированные командные встречи', on_delete=django.db.models.deletion.CASCADE, related_name='team', to='tasks.meeting', verbose_name='встречи'),
        ),
    ]
