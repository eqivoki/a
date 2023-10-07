"""
Django settings for finalGame project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = '/var/data/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ai=u$d7s**l=sfu47^8@rpdlptrl1)z8!o3+v_=d(!5xk6xrg%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


#ALLOWED_HOSTS = ['econ-game.ru', 'www.econ-game.ru', '158.160.26.1']
ALLOWED_HOSTS = ['*']

SECURE_SSL_REDIRECT = False



# Application definition



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Game.apps.GameConfig',
    'debug_toolbar',
    'crispy_forms',
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'finalGame.urls'

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR), 'Game/templates']
        ,
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

WSGI_APPLICATION = 'finalGame.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
            'default': {
                     'ENGINE': 'django.db.backends.postgresql_psycopg2',
                     'NAME': 'economic_game',
                     'USER' : 'master_nikola',
                     'PASSWORD' : 'ksdsff-sdsd323$',
                     'HOST' : 'localhost',
                     'PORT' : '5432',
                        }
            }


DEFAULT_AUTO_FIELD='django.db.models.AutoField'
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'Game/static'),)
STATIC_URL = '/static/'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')