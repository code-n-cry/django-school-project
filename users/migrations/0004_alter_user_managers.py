# Generated by Django 3.2.17 on 2023-04-06 18:10

from django.db import migrations
import users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230406_1921'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.managers.ActiveUserManager()),
            ],
        ),
    ]
