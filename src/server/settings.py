import os
from pathlib import Path

from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='the-most-secret-key')

DEBUG = config('DEBUG', default=False)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_beat',
    'rest_framework',
    'solo',

    'server.apps.configurations',
    'server.apps.products',
    'server.apps.dictionaries',
    'server.apps.notifications',
    'server.apps.telegram',
    'server.apps.payments',
    'server.apps.feedback',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='rich_bot'),
        'USER': config('POSTGRES_USER', default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='postgres'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default=5432, cast=int),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_DIR = [STATIC_DIR]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_title': 'Бот-Богач',
    'site_header': 'Бот-Богач',
    'site_brand': 'Бот-Богач',
    'welcome_sign': 'Бот-Богач',
    'order_with_respect_to': [
        'products',
        'telegram',
        'configurations',
        'notifications',
        'dictionaries',
        'payments',
        'auth',
    ],
}

BOT_TOKEN = config('BOT_TOKEN', default='')

REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/3'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

QUESTIONS_MAX_COUNT = config('QUESTIONS_MAX_COUNT', default=10, cast=int)
NOTIFICATION_TIME = config('NOTIFICATION_TIME', default=11, cast=int)

PRODAMUS_KEY = config('PRODAMUS_KEY', default='')
PRODAMUS_URL = config('PRODAMUS_URL')
