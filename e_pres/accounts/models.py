from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save

ORGANIZATION_CHOICES = (
    ('uoa', 'University of Athens'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    organization = models.CharField(max_length=6, choices=ORGANIZATION_CHOICES, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username





def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        new_profile = UserProfile(user=user)
        new_profile.save()


post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
