from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
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
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("building_detail", kwargs={"pk": self.pk})


class Floor(models.Model):
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=60)
    number = models.PositiveSmallIntegerField()
    blueprint = models.ImageField(upload_to='blueprints/')
    max_evacuation_time = models.PositiveIntegerField(help_text="in seconds",null=True, blank=True)
    stud_number = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("floor_detail", kwargs={"pk": self.pk, "pk_building": self.building.pk})

    def get_building_url(self):
        return reverse("building_detail", kwargs={"pk": self.building.pk})
