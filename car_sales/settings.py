"""
Django settings for car_sales project.
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ========================================== #
# SECURITY & ENVIRONMENT                     #
# ========================================== #

SECRET_KEY = config('SECRET_KEY', default='django-insecure-3l*n0h4*z49)z+6ed6ocpu6xw7s6qh+v_6ze@zfd%ni5u1rl18')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')


# ========================================== #
# APPLICATION DEFINITION                     #
# ========================================== #

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'whitenoise.runserver_nostatic',
    'listings',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_sales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'car_sales.wsgi.application'


# ========================================== #
# DATABASE                                   #
# ========================================== #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'car_sales_db',
        'USER': 'kanjo',
        'PASSWORD': '123456',  # use the password you set
        'HOST': 'localhost',
        'PORT': '5432',              # default PostgreSQL port
    }
}


# ========================================== #
# PASSWORD VALIDATION - REMOVED              #
# ========================================== #

# All password validators are removed to allow any password
AUTH_PASSWORD_VALIDATORS = []


# ========================================== #
# INTERNATIONALIZATION                       #
# ========================================== #

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ========================================== #
# STATIC FILES                               #
# ========================================== #

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ========================================== #
# MEDIA FILES                                #
# ========================================== #

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ========================================== #
# EMAIL CONFIGURATION                        #
# ========================================== #

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ========================================== #
# LOGIN / LOGOUT REDIRECTS                   #
# ========================================== #

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# ========================================== #
# DEFAULT AUTO FIELD                         #
# ========================================== #

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/home/'   # After login, go to the actual homepage
LOGOUT_REDIRECT_URL = '/'       # After logout, go to registration page
