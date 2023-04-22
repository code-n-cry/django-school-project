# Generated by Django 3.2.17 on 2023-04-20 21:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [('users', '0002_remove_user_tasks'), ('users', '0003_comment')]

    dependencies = [
        ('users', '0001_squashed_0002_alter_member_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tasks',
        ),
        migrations.CreateModel(
            name='Comment',
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
                    'content',
                    models.CharField(
                        help_text='содержание вашего комментария(до 50 символов)',
                        max_length=50,
                        verbose_name='содержание',
                    ),
                ),
                (
                    'is_reported',
                    models.BooleanField(
                        default=False,
                        help_text='жаловались ли на комментарий?',
                        verbose_name='жалоба',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        help_text='кто оставил комментарий?',
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='comments',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='автор',
                    ),
                ),
                (
                    'to_user',
                    models.ForeignKey(
                        help_text='кому оставили комментарий?',
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name='received_comments',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='получатель',
                    ),
                ),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
                'default_related_name': 'comments',
            },
        ),
    ]