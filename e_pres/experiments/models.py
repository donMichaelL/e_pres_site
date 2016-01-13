from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from buildings.models import Building

DISASTER_CHOICHES = (
    ('eq', 'Earthquake'),
    ('vl', 'Volcano'),
    ('fl', 'Flood'),
)

class Experiment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=60)
    disaster = models.CharField(max_length=2, choices=DISASTER_CHOICHES)
    execuation_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __unicode__(self):
        return self.name

def return_choices():
    return DISASTER_CHOICHES
