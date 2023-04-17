from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Skill',
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
                        max_length=25,
                        unique=True,
                        verbose_name='название',
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
            ],
            options={
                'verbose_name': 'навык',
                'verbose_name_plural': 'навыки',
                'default_related_name': 'skills',
            },
        ),
    ]
