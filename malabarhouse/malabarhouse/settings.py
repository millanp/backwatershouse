"""
Django settings for malabarhouse project.
<---- Notes ---->
Process of accessing calendar api:
make Credentials,
outof make Http,
outof make service
----> Notes <----
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
from malabarhouse import secret_settings
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
TEMPLATE_DEBUG = True
ADMINS = secret_settings.ADMINS
ALLOWED_HOSTS = ['*']
SITE_URL = "malabarhouse.herokuapp.com"
REGISTRATION_NOTIFICATION_RECIPIENTS = [admin[1] for admin in ADMINS]
EMAIL_HOST = secret_settings.EMAIL_HOST
EMAIL_HOST_USER = secret_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secret_settings.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = 'donotreply@malabarhousereservations.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
LOGIN_REDIRECT_URL = "/"
PAYPAL_RECEIVER_EMAIL = secret_settings.PAYPAL_BUSINESS
PAYPAL_TEST = True
#SESSION_COOKIE_AGE = 30 #I should set this to a reasonable time, not 30 secs
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'registration.supplements.default',
    'registration.contrib.notification',
    'frontend',
    'backend',
    'multiselectfield',
    'paypal.standard.ipn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'malabarhouse.urls'

WSGI_APPLICATION = 'malabarhouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
#     'default': 
}
DATABASES['default'] = dj_database_url.config()
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
