from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from buildings.models import Building, Floor

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

    def get_absolute_url(self):
            return reverse("test_detail", kwargs={"pk": self.pk})


def return_choices():
    return DISASTER_CHOICHES


class Checkpoint(models.Model):
    floor = models.ForeignKey(Floor)
    experiment = models.ForeignKey(Experiment)
    name = models.CharField(max_length=60, null=True, blank=True)
    flux = models.PositiveSmallIntegerField(null=True, blank=True)
    coord_x = models.DecimalField(max_digits=8, decimal_places=3)
    coord_y = models.DecimalField(max_digits=8, decimal_places=3)
    exit = models.BooleanField(default=False)

    def __unicode__(self):
        return self.floor.name