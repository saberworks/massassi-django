from .base import *

DEBUG = False

ALLOWED_HOSTS = ['www.massassi.net', 'massassi.net']

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
            'level': 'ERROR', # change to debug to see queries
            'handlers': ['console'],
            'propagate': False,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
