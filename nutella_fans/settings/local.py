from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = os.getenv("SECRET_KEY")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLED_APPS += ["debug_toolbar", ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
