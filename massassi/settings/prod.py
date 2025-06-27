from .base import *

DEBUG = False

ALLOWED_HOSTS = ['www.massassi.net', 'massassi.net']

CSRF_TRUSTED_ORIGINS=['https://www.massassi.net']

SITE_URL = "https://www.massassi.net"
THREE_DEE_PREVIEW_URL = "https://3dpreview.massassi.net"

# DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

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
