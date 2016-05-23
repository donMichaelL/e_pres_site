from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic import View
from buildings.models import Building
from .models import PreparednessQuestionnaireQuestion, PreparednessQuestionnaire


class PreparednessQuestionnaireView(DetailView):
    model = Building
    template_name = 'dashboard/questionnaires/list_preparednessQuestions.html'

    def get_context_data(self, **kwargs):
        context = super(PreparednessQuestionnaireView, self).get_context_data(**kwargs)
        context['preparedness_questions'] = PreparednessQuestionnaireQuestion.objects.all()
        return context


class PreparednessQuestionnaireNew(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        building = get_object_or_404(Building, pk=kwargs['pk'])
        questionnaire = get_object_or_404(PreparednessQuestionnaire, building=building)
        return JsonResponse('PermissionDenied',status=403, safe=False)
