from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'openfoodfact_db',
        'USER': 'xavgab',
        'PASSWORD': 'openfoodfact',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS += ["debug_toolbar"]
