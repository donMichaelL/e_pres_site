from __future__ import unicode_literals
from django.db import models
from experiments.models import Experiment, Checkpoint
from plans.models import Plan
from tags.models import Tag

class CheckpointReport(models.Model):
    experiment = models.ForeignKey(Experiment)
    checkpoint = models.ForeignKey(Checkpoint)
    current_flux = models.PositiveSmallIntegerField(null=True, blank=True)
    fail = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


    def __unicode__(self):
        return self.experiment.name

ERROR_CODE = (
    ('1', 'Correct Execution'),
    ('2', 'Path Before Path'),
    ('3', 'Teacher'),
)

class CheckpointFailPlan(models.Model):
    experiment = models.ForeignKey(Experiment)
    tag_r = models.ForeignKey(Tag)
    plan = models.ForeignKey(Plan)
    last_current_checkpoint = models.ForeignKey(Checkpoint, null=True, blank=True)
    error_code = models.CharField(max_length=2, choices=ERROR_CODE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    number_of_students_teacher_error = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.experiment.name
