import django.contrib.auth.models
import django.db.models

import users.models


class ActiveUserManager(django.contrib.auth.models.UserManager):
    @classmethod
    def normalize_email(cls, email):
        email = email or ''
        try:
            username, domain = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            username_no_tags = username.split('+')[0].lower()
            if domain.lower() in ['yandex.ru', 'ya.ru']:
                username_no_tags = username_no_tags.replace('.', '-')
                domain = 'yandex.ru'
            if domain.lower() == 'gmail.com':
                username_no_tags = username_no_tags.replace('.', '')
            email = '@'.join([username_no_tags, domain.lower()])
        return email

    def active(self):
        return (
            self.get_queryset()
            .filter(
                is_active=True,
            )
            .only(
                users.models.User.id.field.name,
                users.models.User.username.field.name,
                users.models.User.email.field.name,
                users.models.User.avatar.field.name,
            )
        )

    def public(self):
        return (
            self.get_queryset()
            .filter(
                is_active=True,
                is_visible=True,
            )
            .only(
                users.models.User.id.field.name,
                users.models.User.username.field.name,
                users.models.User.email.field.name,
                users.models.User.avatar.field.name,
            )
        )
