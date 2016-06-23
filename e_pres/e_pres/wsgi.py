"""
WSGI config for e_pres project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise.django import DjangoWhiteNoise
from rednoise import DjangoRedNoise

if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_pres.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_pres.config.production")

application = get_wsgi_application()
if not settings.DEBUG:
    application = DjangoRedNoise(application)
