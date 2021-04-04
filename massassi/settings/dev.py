from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hs$kf9ho&fkofdhx-1hjc-2dad!fm_wpbi9viop5=x42#kzo)!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
        'HOST': 'localhost',
        'PORT': '',
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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
            'level': 'DEBUG',
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
EMAIL_FILE_PATH = '/home/brian/code/massassi-django/emails'  # change this to a proper location

# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
