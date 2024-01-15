import django_heroku
from .base import *
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_KEY = os.getenv("SENTRY_KEY")

sentry_sdk.init(
    dsn="https://b226777f135c4c8993320e079136bd6c@o4504474859536384.ingest.sentry.io/4504474859536384",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com', 'purbeurre.ovh', '161.35.213.37']
SECRET_KEY = os.getenv("SECRET_KEY")


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
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


django_heroku.settings(locals())
