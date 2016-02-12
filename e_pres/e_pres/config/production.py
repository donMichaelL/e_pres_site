from .base import *

DEBUG = True


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
