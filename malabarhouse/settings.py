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

TODO:
1. Add username to nav bar in inner site
2. In account approved email, use logout_then_login link
3. Add some explanation of why user should pay fee
4. Add housekeeping to Booking.__str__
5. Payment complete message
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Switched to Sublime Text
import os

import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
TEMPLATE_DEBUG = True
ADMINS = (('millan', 'millan.philipose@gmail.com'),)
ALLOWED_HOSTS = ['www.backwatershouse.herokuapp.com']
REGISTRATION_NOTIFICATION_RECIPIENTS = [admin[1] for admin in ADMINS]
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = 'donotreply@backwatershousereservations.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
LOGIN_REDIRECT_URL = "/"
PAYPAL_RECEIVER_EMAIL = os.environ['PAYPAL_BUSINESS']
PAYPAL_TEST = True
SITE_URL = "https://backwatershouse.herokuapp.com"
SESSION_COOKIE_AGE = 10 * 60
SESSION_SAVE_EVERY_REQUEST = True
SERVER_EMAIL = "server@backwatershouse.herokuapp.com"
# Application definition
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
SITE_ID = 1
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'paypal.standard.ipn',
    'frontend',
    'backend',
    'floppyforms',
    'dappr',
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
'''
Some random information about the Postgres database
  config /etc/postgresql/9.5/main
  data   /var/lib/postgresql/9.5/main
  locale en_US.UTF-8
  socket /var/run/postgresql
  port   5432
'''
DATABASES = {
    'default': dj_database_url.config()
    #     'default':
}
# DATABASES['default'] = dj_database_url.config()
# DATABASES['default'] = DATABASES[os.environ.get('DJANGO_DATABASE_LABEL', 'default')]
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

BOOKING_FEE = "$5.50"

VENUE_NAME = "Backwaters House"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
