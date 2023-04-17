from django.db import migrations, models

import teams.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('skills', '__first__'),
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
                    'detail',
                    models.TextField(
                        help_text='более подробное описание',
                        null=True,
                        verbose_name='детали',
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
