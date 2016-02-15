from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from experiments.mixins import ContentUserOnlyMixin
from django.views.generic.detail import DetailView
from django.views.generic import View
from experiments.models import Experiment, Checkpoint
from .models import CheckpointReport
from .utils import total_building_students


class PostExperiment(LoginRequiredMixin, ContentUserOnlyMixin, DetailView):
    template_name = 'dashboard/analytics/post_experiment.html'
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(PostExperiment, self).get_context_data(**kwargs)
        context['plans'] = self.object.plan_set.all()
        context['checkpoints'] = Checkpoint.objects.filter(experiment=self.object)
        context['total_student'] = total_building_students(self.object)
        print context['total_student']
        return context

class ReportFluxPostExperiment(View):
    def get(self, request, *args, **kwargs):
        experiment = Experiment.objects.get(pk=kwargs['pk_experiment'])
        checkpoint = Checkpoint.objects.get(pk=kwargs['pk'])
        report = CheckpointReport.objects.filter(experiment=experiment).filter(checkpoint=checkpoint)
        return JsonResponse(serializers.serialize('json', report), safe=False)
