import os
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    interpolate=True,
    SECRET_KEY=(str, 'not-a-secret'),
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['*']),
    FROM_EMAIL=(str, 'noreply@example.com'),
    MAX_LOGIN_AMOUNT=(int, 5),
    USER_ACTIVE_DEFAULT=(bool, False),
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'ckeditor',
    'debug_toolbar',
    'django_cleanup.apps.CleanupConfig',
    'django_dump_load_utf8',
    'sorl.thumbnail',
    'tasks.apps.TasksConfig',
    'teams.apps.TeamsConfig',
    'users.apps.UsersConfig',
    'homepage.apps.HomepageConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'lyceum.middleware.middlewares.TimezoneMiddleware',
]

ROOT_URLCONF = 'lyceum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lyceum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


INTERNAL_IPS = ['127.0.0.1']

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.' 'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

USER_ACTIVE_DEFAULT = env('USER_ACTIVE_DEFAULT')


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

DATE_FORMAT = 'd-m-Y'

USE_L10N = False

USE_TZ = True


MAX_LOGIN_AMOUNT = env('MAX_LOGIN_AMOUNT')

AUTHENTICATION_BACKENDS = ('users.backends.EmailBackend',)

LOGIN_URL = '/auth/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/auth/login/'

AUTH_USER_MODEL = 'users.User'

LANGUAGES = [
    ('ru', gettext_lazy('Russian')),
    ('en', gettext_lazy('English')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale/'),)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = BASE_DIR / 'send_mail'

FROM_EMAIL = env('FROM_EMAIL')

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

CKEDITOR_CONFIGS = {
    'item_text_editor': {
        'toolbar': 'full',
    },
}
