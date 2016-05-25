from django.shortcuts import render, get_object_or_404
import json
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic import View
from buildings.models import Building
from experiments.models import Experiment
from .models import PreparednessQuestionnaireQuestion, PreparednessQuestionnaireAnswer, EvaluationQuestionnaireQuestion, EvaluationQuestionnaireAnswer, EvaluationStudentsQuestionnaire, EvaluationStudentsQuestionnaireAnswer


class PreparednessQuestionnaireView(DetailView):
    model = Building
    template_name = 'dashboard/questionnaires/list_preparednessQuestions.html'

    def get_context_data(self, **kwargs):
        context = super(PreparednessQuestionnaireView, self).get_context_data(**kwargs)
        context['preparedness_questions'] = PreparednessQuestionnaireQuestion.objects.all()
        return context


class PreparednessQuestionnaireNew(View):
    def post(self, request, *args, **kwargs):
        building = get_object_or_404(Building, pk=kwargs['pk'])
        answers = request.POST.get('answers')
        dicto = json.loads(answers)
        for question_id, answer in dicto.iteritems():
            question = get_object_or_404(PreparednessQuestionnaireQuestion, pk=question_id)
            obj, created = PreparednessQuestionnaireAnswer.objects.get_or_create(building=building, question=question)
            obj.answer = answer
            obj.save()
        return JsonResponse('ok', status=200, safe=False)


class EvaluationQuestionnaireView(DetailView):
    model = Experiment
    template_name = 'dashboard/questionnaires/list_evacuationQuestions.html'

    def get_context_data(self, **kwargs):
        context = super(EvaluationQuestionnaireView, self).get_context_data(**kwargs)
        context['evacuation_questions'] = EvaluationQuestionnaireQuestion.objects.all()
        return context


class EvaluationQuestionnaireNew(View):
    def post(self, request, *args, **kwargs):
        experiment = get_object_or_404(Experiment, pk=kwargs['pk'])
        answers = request.POST.get('answers')
        dicto = json.loads(answers)
        for question_id, answer in dicto.iteritems():
            question = get_object_or_404(EvaluationQuestionnaireQuestion, pk=question_id)
            obj, created = EvaluationQuestionnaireAnswer.objects.get_or_create(experiment=experiment, question=question)
            obj.answer = answer
            obj.save()
        return JsonResponse('ok', status=200, safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class EvaluationStudentsQuestionnaireView(View):
    def get(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        experiment = get_object_or_404(Experiment, pk=kwargs['pk'])
        context = {};
        already_answred = EvaluationStudentsQuestionnaireAnswer.objects.filter(experiment=experiment, ip=ip).count()
        if already_answred:
            context['answered'] = True
        else:
            questions = EvaluationStudentsQuestionnaire.objects.all()
            context['experiment'] = experiment  
            context['questions'] = questions
        return render(request, 'student_questionnaire.html', context)

    def post(self, request, *args, **kwargs):
        print 'hello'
        ip = get_client_ip(request)
        experiment = get_object_or_404(Experiment, pk=kwargs['pk'])
        already_answred = EvaluationStudentsQuestionnaireAnswer.objects.filter(experiment=experiment, ip=ip).count()
        if already_answred:
            return JsonResponse('ok', status=200, safe=False)
        else:
            answers = request.POST.get('answers')
            dicto = json.loads(answers)
            for question_id, answer in dicto.iteritems():
                question = get_object_or_404(EvaluationStudentsQuestionnaire, pk=question_id)
                obj, created = EvaluationStudentsQuestionnaireAnswer.objects.get_or_create(experiment=experiment, question=question, ip=ip)
                obj.answer = answer
                obj.save()
            return JsonResponse('ok', status=200, safe=False)


class EvaluationStudentsQuestionnaireNew(View):
    pass
