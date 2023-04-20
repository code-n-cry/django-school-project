import django.core.mail
import django.utils.timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.translation import gettext_lazy

from users.managers import ActiveUserManager


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            normalized_email = ActiveUserManager.normalize_email(username)
            user = user_model.objects.get(
                Q(email=normalized_email) | Q(username=username)
            )
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(
                user
            ):
                user.failed_logins = 0
                user.save()
                return user
            if not user.check_password(password):
                user.failed_logins += 1
                user.last_failed_login_date = django.utils.timezone.now()
                user.save()
                if user.failed_logins >= settings.MAX_LOGIN_AMOUNT:
                    user.is_active = False
                    user.save()
                    email_text = gettext_lazy(
                        ''.join(
                            [
                                'Совершено много неудачных попыток входа в '
                                'Ваш аккаунт! Для безопасности он был отк',
                                'лючён.\nВаша ссылка для восстановления: ',
                            ]
                        )
                    )
                    if request:
                        email_text += request.build_absolute_uri(
                            django.urls.reverse(
                                'auth:recover',
                                kwargs={'username': user.get_username()},
                            )
                        )
                    else:
                        email_text += (
                            'http://127.0.0.1:8000'
                            + django.urls.reverse(
                                'auth:recover',
                                kwargs={'username': user.get_username()},
                            )
                        )
                    django.core.mail.send_mail(
                        gettext_lazy('Восстановление'),
                        email_text,
                        settings.FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
        return None
