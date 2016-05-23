from django.shortcuts import render
from django.views.generic.list import ListView
from .models import PreparednessQuestionnaireQuestion


class PreparednessQuestionnaireView(ListView):
    model = PreparednessQuestionnaireQuestion
    template_name = 'dashboard/questionnaires/list_preparednessQuestions.html'
