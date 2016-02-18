from __future__ import unicode_literals
from django.db import models
from experiments.models import Experiment, Checkpoint
from plans.models import Plan

class CheckpointReport(models.Model):
    experiment = models.ForeignKey(Experiment)
    checkpoint = models.ForeignKey(Checkpoint)
    current_flux = models.PositiveSmallIntegerField(null=True, blank=True)
    fail = models.BooleanField(default=False)

    def __unicode__(self):
        return self.experiment.name


class CheckpointFailPlan(models.Model):
    experiment = models.ForeignKey(Experiment)
    plan = models.ForeignKey(Plan)
    last_current_checkpoint = models.ForeignKey(Checkpoint)
    tag = models.IntegerField()

    def __unicode__(self):
        return self.experiment.name
