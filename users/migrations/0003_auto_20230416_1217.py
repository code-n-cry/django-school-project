import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0001_squashed_0005_delete_invite'),
        ('users', '0002_auto_20230410_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='lead_teams',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tasks',
        ),
        migrations.RemoveField(
            model_name='user',
            name='teams',
        ),
        migrations.CreateModel(
            name='Member',
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
                    'is_lead',
                    models.BooleanField(
                        default=False,
                        help_text='является ли участник лидом',
                        verbose_name='лид',
                    ),
                ),
                (
                    'team',
                    models.ForeignKey(
                        help_text='команда, в которой состоит юзер',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='members',
                        to='teams.team',
                        verbose_name='команда',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        help_text='юзер',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='member',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='пользователь',
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='member',
            constraint=models.UniqueConstraint(
                fields=('team', 'user'), name='unique_member'
            ),
        ),
    ]
