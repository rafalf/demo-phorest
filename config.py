import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
IMG_DIR = os.path.join(STATIC_DIR, 'img')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'download')
BASE_URL = "https://phorest.com/"
BOOK_SALONS_URL = "https://phorest.com/book/salons/demo-uk"
SIGNUP_URL = "https://staging.cogsworth.com/app/signup"
LOGIN_URL = "https://staging.cogsworth.com/app/signup"

LOGGING_CONFIG = {
    'formatters': {
        'brief': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'brief',
            'filename': 'tests.log',
            'maxBytes': 1024*1024,
            'backupCount': 3,
        },
    },
    'loggers': {
        'main': {
            'propagate': False,
            'handlers': ['console', 'file'],
            'level': 'INFO'
        }
    },
    'version': 1
}