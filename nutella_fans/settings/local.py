from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = os.getenv("SECRET_KEY")
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
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INSTALLED_APPS += ["debug_toolbar"]
