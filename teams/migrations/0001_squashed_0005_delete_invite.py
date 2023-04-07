# Generated by Django 3.2.17 on 2023-04-07 18:36

import django.db.models.deletion
from django.db import migrations, models

import teams.models


class Migration(migrations.Migration):
    replaces = [
        ('teams', '0001_squashed_0005_alter_team_skills'),
        ('teams', '0002_auto_20230407_1533'),
        ('teams', '0003_auto_20230407_1535'),
        ('teams', '0004_remove_invite_to_team'),
        ('teams', '0005_delete_invite'),
    ]

    initial = True

    dependencies = [
        ('tasks', '0001_squashed_0002_auto_20230406_2110'),
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
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
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text='когда создана команда?',
                        verbose_name='дата создания',
                    ),
                ),
                (
                    'is_open',
                    models.BooleanField(
                        default=True,
                        help_text='показывается ли ваша команда в поиске?',
                        verbose_name='открытость',
                    ),
                ),
                (
                    'tasks',
                    models.ForeignKey(
                        blank=True,
                        help_text='задания для команды',
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='team',
                        to='tasks.task',
                        verbose_name='задания',
                    ),
                ),
                (
                    'avatar',
                    models.ImageField(
                        blank=True,
                        help_text='картинка профиля команды',
                        null=True,
                        upload_to=teams.models.avatar_image_path,
                        verbose_name='аватарка',
                    ),
                ),
                (
                    'detail',
                    models.TextField(
                        help_text='более подробное описание',
                        null=True,
                        verbose_name='детали',
                    ),
                ),
                (
                    'meetings',
                    models.ForeignKey(
                        blank=True,
                        help_text='запланированные командные встречи',
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='team',
                        to='tasks.meeting',
                        verbose_name='встречи',
                    ),
                ),
                (
                    'unique_name',
                    models.CharField(
                        editable=False,
                        help_text='Колонка для проверки уникальности названия',
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name='уникальное имя',
                    ),
                ),
                (
                    'skills',
                    models.ManyToManyField(
                        help_text='какие навыки нужны команде?',
                        related_name='team',
                        to='skills.Skill',
                        verbose_name='требуемые навыки',
                    ),
                ),
            ],
            options={
                'verbose_name': 'команда',
                'verbose_name_plural': 'команды',
                'default_related_name': 'team',
            },
        ),
    ]