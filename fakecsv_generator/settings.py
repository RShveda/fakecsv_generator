"""
Django settings for fakecsv_generator project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'
SCHEMAS_DIR = BASE_DIR / 'schemas/templates/schemas'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '_h^6usgntj@0!$9sjc5m-^#10w2mdaandh_zwd+p_n8+90$5&v'

import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '_h^6usgntj@0!$9sjc5m-^#10w2mdaandh_zwd+p_n8+90$5&v')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ["csv-generator.herokuapp.com", '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'cloudinary',
    'bootstrap4',
    'schemas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fakecsv_generator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, SCHEMAS_DIR],
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

WSGI_APPLICATION = 'fakecsv_generator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_DIR = BASE_DIR / 'static'
STATICFILES_DIRS = [STATIC_DIR, ]

# Media files

MEDIA_DIR = BASE_DIR / 'media'
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

# Auth urls

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "/"

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Celery configs
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", 'django-db')
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_CONTENT_ENCODING = 'utf-8'
CELERY_ENABLE_REMOTE_CONTROL = False
CELERY_SEND_EVENTS = False
CELERY_TIMEZONE = 'Europe/Kiev'

# Cloudinary settings for Django. Add to your settings file.
CLOUDINARY = {
  'cloud_name': 'ha1dnhqfb',
  'api_key': '851921685312127',
  'api_secret': 'YuJxrZ0K99XAriqdQHOst2IIXlY',
}
