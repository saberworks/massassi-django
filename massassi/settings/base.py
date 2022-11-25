import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Sensitive config values should be set in environment variables rather than
# in the settings files.
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'You must set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'sotd.apps.SotdConfig',
    'users.apps.UsersConfig',
    'levels.apps.LevelsConfig',
    'lotw.apps.LotwConfig',
    'news.apps.NewsConfig',
    'holiday.apps.HolidayConfig',
    'saberworks.apps.SaberworksConfig',
    'imagekit',
    'corsheaders',
    'colorfield',
    'django_s3_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'massassi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR) + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'massassi.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# media files (uploaded images???)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/massassi-user-data/media/'

# css, main site images, etc.
STATIC_URL = '/jedibird-static/'
STATIC_ROOT = '/jedibird-static/';

LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'

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
    'formatters': {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s %(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '*': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

AUTH_USER_MODEL = 'users.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SENDGRID_API_KEY = get_env_variable('SENDGRID_API_KEY')

DEFAULT_FROM_EMAIL = 'The Massassi Temple <massassi.temple@gmail.com>'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# SECURITY WARNING: don't allow too many fields in production
DATA_UPLOAD_MAX_NUMBER_FIELDS = 50
DATA_UPLOAD_MAX_MEMORY_SIZE = 1073741824 # 1GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 1073741824 # 1GB

# S3 settings for saberworks user-uploaded files.
# The AWS region to connect to.
AWS_REGION = "us-west-2"
AWS_BUCKET_SABERWORKS = get_env_variable('AWS_BUCKET_SABERWORKS')
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_AUTH = False

# Anything in here will be available to TEMPLATES so be careful
SETTINGS_EXPORT = [
    'SITE_URL',
    'THREE_DEE_PREVIEW_URL',
]
