from django.shortcuts import render
from django.views.generic.detail import DetailView
from buildings.models import Building
from .models import PreparednessQuestionnaireQuestion


class PreparednessQuestionnaireView(DetailView):
    model = Building
    template_name = 'dashboard/questionnaires/list_preparednessQuestions.html'

    def get_context_data(self, **kwargs):
        context = super(PreparednessQuestionnaireView, self).get_context_data(**kwargs)
        context['preparedness_questions'] = PreparednessQuestionnaireQuestion.objects.all()
        return context
