from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from buildings.models import Building
from .models import Experiment, Checkpoint
from .forms import ExperimentForm, CheckpointForm
from .mixins import ContentUserOnlyMixin, CheckpointContentUserOnlyMixin

class ExperimentListView(LoginRequiredMixin, ListView):
    model = Experiment
    template_name = 'dashboard/experiments/list_experiment.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Experiment.objects.all()
        return Experiment.objects.filter(user=self.request.user)


class ExperimentNewView(LoginRequiredMixin, FormView):
    form_class = ExperimentForm
    template_name = 'dashboard/experiments/new_experiment.html'

    def get_form(self, *args, **kwargs):
        form = super(ExperimentNewView, self).get_form(*args, **kwargs)
        if self.request.user.is_superuser:
            form.fields['building'].queryset = Building.objects.all()
        else:
            form.fields['building'].queryset = Building.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        test = form.save(commit=False)
        test.user = self.request.user
        test.save()
        messages.success(self.request, ' %s was created.'% test.name )
        return super(ExperimentNewView, self).form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('experiment_list')


class ExperimentDeleteView(LoginRequiredMixin, ContentUserOnlyMixin, DeleteView):
    model = Experiment
    template_name = 'dashboard/experiments/experiment_delete.html'

    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('experiment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, ' %s was deleted.'% self.get_object().name)
        return super(ExperimentDeleteView, self).delete(request, *args, **kwargs)


class ExperimentDetailView(LoginRequiredMixin, ContentUserOnlyMixin, UpdateView, DetailView):
    template_name = 'dashboard/experiments/experiment_detail.html'
    form_class = ExperimentForm
    model = Experiment

    def form_valid(self, form):
        messages.success(self.request, ' %s was updated.'% form.cleaned_data['name'] )
        return super(ExperimentDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ExperimentDetailView, self).get_context_data(**kwargs)
        context['checkpoint_form'] = CheckpointForm()
        context['checkpoints'] = Checkpoint.objects.filter(experiment=self.object)
        return context


class PostExperiment(LoginRequiredMixin, ContentUserOnlyMixin, DetailView):
    template_name = 'dashboard/experiments/post_experiment.html'
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(PostExperiment, self).get_context_data(**kwargs)
        context['plans'] = self.object.plan_set.all()
        context['checkpoints'] = Checkpoint.objects.filter(experiment=self.object)
        return context

class CheckpointInsertView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CheckpointForm(request.POST)
        experiment = get_object_or_404(Experiment, pk=kwargs['pk'])
        if experiment.building.user != request.user:
            if not request.user.is_superuser:
             return PermissionDenied()
        if form.is_valid():
            pk = form.cleaned_data['pk']
            if pk:
                checkpoint = get_object_or_404(Checkpoint, pk=pk)
                new_form = CheckpointForm(request.POST, instance=checkpoint)
                new_form.save()
                messages.success(self.request, 'Checkpoint: %s was updated.'% checkpoint.pk )
            else:
                checkpoint = form.save()
                messages.success(self.request, 'Checkpoint: %s was created.'% checkpoint.pk )
        else:
            print form.errors
        return redirect(reverse_lazy('experiment_detail', kwargs={'pk': kwargs['pk']}))


class CheckpointDeleteView(LoginRequiredMixin, CheckpointContentUserOnlyMixin, DeleteView):
    model = Checkpoint
    template_name = 'dashboard/experiments/checkpoint_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Checkpoint %s was deleted.'% self.get_object().pk)
        return super(CheckpointDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_experiment_absolute_url()
