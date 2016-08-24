from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from experiments.mixins import ContentUserOnlyMixin
from django.views.generic.detail import DetailView
from django.views.generic import View
from experiments.models import Experiment, Checkpoint
from .models import CheckpointReport
from .utils import total_building_students
from django.core.exceptions import PermissionDenied


class PostExperiment(LoginRequiredMixin, ContentUserOnlyMixin, DetailView):
    template_name = 'dashboard/analytics/post_experiment.html'
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(PostExperiment, self).get_context_data(**kwargs)
        context['plans'] = self.object.plan_set.all()
        context['checkpoints'] = Checkpoint.objects.filter(experiment=self.object)
        context['total_student'] = total_building_students(self.object)
        context['total_evacuation_time'] = self.object.evacuation_time / 60
        return context


# JSON
class ReportFluxPostExperiment(View):
    def get(self, request, *args, **kwargs):
        experiment = get_object_or_404(Experiment, pk=kwargs['pk_experiment'])
        checkpoint = get_object_or_404(Checkpoint, pk=kwargs['pk'])
        report = CheckpointReport.objects.filter(experiment=experiment).filter(checkpoint=checkpoint)
        if request.user == experiment.building.user or request.user.is_superuser:
            return JsonResponse(serializers.serialize('json', report), safe=False)
        return JsonResponse('PermissionDenied',status=403, safe=False)


class RealTimeView(LoginRequiredMixin, ContentUserOnlyMixin, DetailView):
    template_name = 'dashboard/analytics/realtime.html'
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(RealTimeView, self).get_context_data(**kwargs)
        context['plans'] = self.object.plan_set.all()
        context['checkpoints'] = Checkpoint.objects.filter(experiment=self.object)
        context['total_student'] = total_building_students(self.object)
        return context
