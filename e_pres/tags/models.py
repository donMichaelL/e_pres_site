from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class Tag(models.Model):
    tag_string = models.TextField(unique=True)
    teacher = models.ForeignKey('Tag', related_name='leader', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.tag_string
