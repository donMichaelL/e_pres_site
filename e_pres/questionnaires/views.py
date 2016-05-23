from django.shortcuts import render
from django.views.generic.list import ListView
from .models import EvaluationQuestionnaireQuestion


class EvacuationQuestionnaireView(ListView):
    model = EvaluationQuestionnaireQuestion
    template_name = 'dashboard/questionnaires/list_questions.html'
