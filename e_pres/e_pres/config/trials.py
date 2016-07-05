from .base import *

DEBUG = True

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


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
