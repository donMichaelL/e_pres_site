from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class Tag(models.Model):
    tag_id = models.CharField(max_length=70)
    teacher = models.ForeignKey('Tag', related_name='leader')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.name
