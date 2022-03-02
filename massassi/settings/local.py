from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS=['http://*', 'https://*', 'http://localhost:3000']

CORS_ALLOWED_ORIGINS=['http://localhost:3000', 'http://localhost:4173']
CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[DJANGO] %(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG', # change to debug to see queries
            'handlers': ['console'],
            'propagate': False,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
