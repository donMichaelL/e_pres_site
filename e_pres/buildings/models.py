from __future__ import unicode_literals
from django.db import models
from django.conf import settings

COUNTRIES_CHOICES = (
    ('gr', 'Greece'),
    ('rm', 'Romania'),
)


class Building(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=80)
    country = models.CharField(max_length=2, choices=COUNTRIES_CHOICES)
    address = models.CharField(max_length=30, null=True, blank=True)
    tk = models.PositiveIntegerField(null=True, blank=True)
    max_evacuation_time = models.PositiveIntegerField(help_text="in seconds",null=True, blank=True)
    photo = models.ImageField(upload_to='building_images/', null=True, blank=True)


    def __unicode__(self):
        return self.user.username
