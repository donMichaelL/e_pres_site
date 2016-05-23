from __future__ import unicode_literals
from buildings.models import Building
from django.db import models

ANSWERS_CHOICES = (
    ('yes', 'YES'),
    ('no', 'NO')
)

class PreparednessQuestionnaireQuestion(models.Model):
    question = models.CharField(max_length=240)

    def __unicode__(self):
        return self.question

class PreparednessQuestionnaire(models.Model):
    building = models.OneToOneField(Building)

    def __unicode__(self):
        return self.building.name

class PreparednessQuestionnaireAnswer(models.Model):
    questionnaire = models.ForeignKey(PreparednessQuestionnaire)
    question = models.ForeignKey(PreparednessQuestionnaireQuestion)
    answer = models.CharField(max_length=3, choices=ANSWERS_CHOICES)

    class Meta:
        unique_together = ('questionnaire', 'question',)

    def __unicode__(self):
        return self.questionnaire.__unicode__()
