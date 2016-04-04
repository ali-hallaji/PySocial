"""
Django settings for pysocial project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from ConfigParser import RawConfigParser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

config = RawConfigParser()
config.read(BASE_DIR + '/pysocial/settings.ini')

ON_PYSOCIAL_HOST = config.getboolean('host', 'ON_PYSOCIAL')

DJANGO_DB_NAME = config.get('django_db', 'DATABASE_NAME')
DJANGO_DB_USER = config.get('django_db', 'DATABASE_USER')
DJANGO_DB_PASSWD = config.get('django_db', 'DATABASE_USER')
DJANGO_DB_HOST = config.get('django_db', 'DATABASE_HOST')
DJANGO_DB_PORT = config.get('django_db', 'DATABASE_PORT')

MONGO_DB_NAME = config.get('mongodb', 'DATABASE_NAME')

if ON_PYSOCIAL_HOST:
    MONGO_DB_URL = config.get('mongodb', 'DATABASE_URL')
else:
    MONGO_DB_URL = "mongodb://localhost:27017"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secrets', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('debug', 'DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pysocial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SETTINGS_PATH, 'templates'),
        ],
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

WSGI_APPLICATION = 'pysocial.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


if not ON_PYSOCIAL_HOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DJANGO_DB_NAME,
            'USER': DJANGO_DB_USER,
            'PASSWORD': DJANGO_DB_PASSWD,
            'HOST': DJANGO_DB_HOST,
            'PORT': DJANGO_DB_PORT
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fa-IR'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

# Custome App
INSTALLED_APPS += [
    'users',
]

# Email Configurations
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = config.get('email', 'MAILGUN_KEY')
MAILGUN_SERVER_NAME = config.get('email', 'MAILGUN_URL')

try:
    from settings_local import *

except Exception as e:
    raise Exception(e)
