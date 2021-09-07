import django_heroku
from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com']
# SECRET_KEY = os.getenv("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nutella_fans.base.apps.BaseConfig',
    'nutella_fans.product.apps.ProductConfig',
    'nutella_fans.save_substitute.apps.SaveSubstituteConfig',
    'nutella_fans.users_account.apps.UsersAccountConfig',
]

django_heroku.settings(locals())
