# Generated by Django 3.2.17 on 2023-04-18 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0002_alter_member_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tasks',
        ),
    ]
