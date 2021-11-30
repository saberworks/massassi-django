from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't allow this many fields in production
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'massassi',
        'USER': 'massassi',
        'PASSWORD': get_env_variable('MASSASSI_DATABASE_PASSWORD'),
        'HOST': get_env_variable('MASSASSI_DATABASE_HOST'),
        'PORT': '',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'loggers': {
        'asyncio': {
            'level': 'WARNING',
        },
        'django.db.backends': {
            'level': 'WARNING', # change to debug to see queries
            'handlers': ['console'],
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/home/brian/code/m2/emails'  # change this to a proper location
