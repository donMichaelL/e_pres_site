from __future__ import unicode_literals
from django.db import models
from experiments.models import Experiment, Checkpoint


class CheckpointReport(models.Model):
    experiment = models.ForeignKey(Experiment)
    checkpoint = models.ForeignKey(Checkpoint)
    current_flux = models.PositiveSmallIntegerField(null=True, blank=True)
    fail = models.BooleanField(default=False)

    def __unicode__(self):
        return self.experiment.name
