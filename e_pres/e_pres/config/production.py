from .base import *

DEBUG = False

ALLOWED_HOSTS = ['.hawk1.di.uoa.gr']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': get_secret('PRODUCTION_DATABASE_USER'),
        'PASSWORD': get_secret('PRODUCTION_DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
