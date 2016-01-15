from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from .models import Experiment, Checkpoint
from .forms import ExperimentForm, CheckpointForm

class ExperimentListView(ListView):
    model = Experiment
    template_name = 'dashboard/experiments/list_tests.html'

    def get_queryset(self):
        return Experiment.objects.filter(user=self.request.user)


class ExperimentNewView(FormView):
    form_class = ExperimentForm
    template_name = 'dashboard/experiments/new_test.html'

    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('test_list')

    def form_valid(self, form):
        test = form.save(commit=False)
        test.user = self.request.user
        test.save()
        return super(ExperimentNewView, self).form_valid(form)


class ExperimentDeleteView(DeleteView):
    model = Experiment
    template_name = 'dashboard/experiments/test_delete.html'

    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('test_list')


class ExperimentDetailView(UpdateView, DetailView):
    template_name = 'dashboard/experiments/experiment_detail.html'
    form_class = ExperimentForm
    model = Experiment

    def get_context_data(self, **kwargs):
        context = super(ExperimentDetailView, self).get_context_data(**kwargs)
        context['checkpoint_form'] = CheckpointForm()
        context['checkpoints'] = Checkpoint.objects.filter(experiment=self.object)
        return context


class CheckpointInsertView(View):
    def post(self, request, *args, **kwargs):
        form = CheckpointForm(request.POST)
        if form.is_valid():
            print form.cleaned_data['exit']
            pk = form.cleaned_data['pk']
            if pk:
                checkpoint = get_object_or_404(Checkpoint, pk=pk)
                new_form = CheckpointForm(request.POST, instance=checkpoint)
                new_form.save()
            else:
                form.save()
        else:
            print form.errors
        return redirect('/experiments/1')


class CheckpointDeleteView(DeleteView):
    model = Checkpoint
    template_name = 'dashboard/experiments/checkpoint_delete.html'

    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('test_list')
