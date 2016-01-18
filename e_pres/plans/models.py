from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from experiments.models import Experiment


class Plan(models.Model):
    experiment = models.ForeignKey(Experiment)
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plan_detail", kwargs={"pk": self.pk, "pk_experiment": self.experiment.pk})
