from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '[::1]']
SECRET_KEY = os.getenv("SECRET_KEY")


INSTALLED_APPS += ["debug_toolbar", ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
