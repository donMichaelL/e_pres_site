from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from experiments.models import Experiment, Checkpoint
from tags.models import Tag


class Plan(models.Model):
    experiment = models.ForeignKey(Experiment)
    name = models.CharField(max_length=60)
    before = models.ForeignKey('self',verbose_name="Execute after plath", null=True, blank=True)
    max_evacuation_time = models.PositiveIntegerField(verbose_name="Maximum Evacuation Time in Sec",null=True, blank=True, default=0)
    tag_leader = models.ForeignKey(Tag, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plan_detail", kwargs={"pk": self.pk, "pk_experiment": self.experiment.pk})

    @property
    def get_correct_execution_failures(self):
        return self.returnFailureResults(1)

    @property
    def get_path_after_path_failures(self):
        return self.returnFailureResults(2)

    @property
    def get_teacher_failures(self):
        return self.returnFailureResults(3)

    def returnFailureResults(self, error_code):
        results = []
        correct_execution = self.checkpointfailplan_set.filter(error_code=error_code)
        for failure in correct_execution:
            sequence = failure.last_current_checkpoint.sequence if failure.last_current_checkpoint != None else "Starting"
            found = False
            for result in results:
                if result['sequence'] == sequence:
                    result['tag'].append(failure.tag_r.tag_string)
                    found = True
                    break
            if not found:
                results.append({
                    'sequence': sequence,
                    'tag': [failure.tag_r.tag_string]
                })
        return results

class Connection(models.Model):
    plan = models.ForeignKey(Plan)
    checkpoint = models.ForeignKey(Checkpoint)
    seq = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.plan.name

    class Meta:
        ordering = ["seq"]
