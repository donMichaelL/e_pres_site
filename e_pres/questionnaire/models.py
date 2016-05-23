from __future__ import unicode_literals
from buildings.models import Building
from django.db import models

ANSWERS_CHOICES = (
    ('yes', 'YES'),
    ('no', 'NO')
)

class EvaluationQuestionnaireQuestion(models.Model):
    question = models.CharField(max_length=240)

    def __unicode__(self):
        return self.question

class EvacuationQuestionnaire(models.Model):
    building = models.OneToOneField(Building)

    def __unicode__(self):
        return self.building.name

class EvacuationQuestionnaireAnswer(models.Model):
    questionnaire = models.ForeignKey(EvacuationQuestionnaire)
    question = models.ForeignKey(EvaluationQuestionnaireQuestion)
    answer = models.CharField(max_length=3, choices=ANSWERS_CHOICES)

    class Meta:
        unique_together = ('questionnaire', 'question',)

    def __unicode__(self):
        return self.questionnaire.__unicode__()