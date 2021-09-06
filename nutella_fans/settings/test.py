from .base import *

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
