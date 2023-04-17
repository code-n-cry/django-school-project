import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='team',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tasks',
                to='teams.team',
                verbose_name='команда',
            ),
        ),
        migrations.AddField(
            model_name='meeting',
            name='team',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='meetings',
                to='teams.team',
                verbose_name='команда',
            ),
        ),
    ]
