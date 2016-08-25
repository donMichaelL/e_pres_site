from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from experiments.mixins import ContentUserOnlyMixin
from django.views.generic.detail import DetailView
from django.views.generic import View
from experiments.models import Experiment, Checkpoint
from .models import CheckpointReport, CheckpointFailPlan
from .utils import total_building_students
from django.core.exceptions import PermissionDenied


class PostExperimentView(LoginRequiredMixin, ContentUserOnlyMixin, DetailView):
    template_name = 'dashboard/analytics/post_experiment.html'
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(PostExperimentView, self).get_context_data(**kwargs)
        context['plans'] = self.object.plan_set.all()
        context['checkpoints'] = Checkpoint.objects.filter(experiment=self.object)
        context['total_student'] = total_building_students(self.object)
        if self.object.evacuation_time:
            context['total_evacuation_time'] = self.object.evacuation_time / 60
        return context


class PostExperimentDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        experiment = get_object_or_404(Experiment, pk=kwargs['pk'])
        return render(request, 'dashboard/analytics/analytics_delete.html', {'experiment': experiment})

    def post(self, request, *args, **kwargs):
        experiment = get_object_or_404(Experiment, pk=kwargs['pk'])
        CheckpointReport.objects.filter(experiment=experiment).delete()
        CheckpointFailPlan.objects.filter(experiment=experiment).delete()
        experiment.finished = False
        experiment.save()
        messages.success(self.request, ' %s deleted analytics'% experiment.name)
        return HttpResponseRedirect(reverse_lazy('building_detail', kwargs={'pk': experiment.building.pk}))


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
