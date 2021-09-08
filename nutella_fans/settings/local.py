from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = os.getenv("SECRET_KEY")


INSTALLED_APPS += ["debug_toolbar", ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
