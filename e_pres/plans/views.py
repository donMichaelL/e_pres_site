from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from django.forms import formset_factory
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from experiments.models import Experiment, Checkpoint
from .models import Plan, Connection
from .forms import PlanForm, ConnectionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ContentUserOnlyMixin


class PlanNewView(LoginRequiredMixin, ContentUserOnlyMixin, CreateView):
    model = Plan
    template_name = 'dashboard/plans/new_plan.html'
    #fields = ['name', 'before']
    form_class = PlanForm

    def get_success_url(self):
        if self.request.GET.get('next', ''):
            if self.request.GET.get('next', '') == 'new_object':
                return reverse_lazy('plan_detail', kwargs={'pk_experiment': self.object.experiment.pk, 'pk': self.object.pk})
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('experiment_list')

    def get_context_data(self, **kwargs):
        context = super(PlanNewView, self).get_context_data(**kwargs)
        context['test'] = self.kwargs['pk_experiment']
        return context

    def get_form(self, form_class):
        form = super(PlanNewView, self).get_form(form_class)
        experiment = get_object_or_404(Experiment, pk=self.kwargs['pk_experiment'])
        form.fields['before'].choices = [("", "---------"),] + [(plan.pk, plan.name) for plan in experiment.plan_set.all()]
        return form

    def form_valid(self, form):
        plan = form.save(commit=False)
        experiment = get_object_or_404(Experiment, pk=self.kwargs['pk_experiment'])
        plan.experiment = experiment
        plan.save()
        messages.success(self.request, ' %s was created.'% plan.name )
        return super(PlanNewView, self).form_valid(form)


class PlanDetailView(LoginRequiredMixin, ContentUserOnlyMixin, UpdateView, DetailView):
    template_name = 'dashboard/plans/plan_detail.html'
    form_class = PlanForm
    model = Plan

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PlanDetailView, self).get_context_data(**kwargs)
        ConnectionFormSet = formset_factory(ConnectionForm, extra=0)
        context['formset'] = ConnectionFormSet()
        context['empty_plan'] = False if self.object.connection_set.all().count() else True
        context['other_plans'] = Plan.objects.filter(experiment=self.object.experiment).exclude(pk=self.object.pk)
        return context

    def get_form(self, form_class):
        form = super(PlanDetailView, self).get_form(form_class)
        experiment = get_object_or_404(Experiment, pk=self.kwargs['pk_experiment'])
        form.fields['before'].choices = [("", "---------"),] + [(plan.pk, plan.name) for plan in experiment.plan_set.exclude(pk=self.get_object().pk)]
        return form

    def form_valid(self, form):
        messages.success(self.request, ' %s was updated.'% form.cleaned_data['name'] )
        return super(PlanDetailView, self).form_valid(form)


class PlanDeleteView(LoginRequiredMixin, ContentUserOnlyMixin, DeleteView):
    model = Plan
    template_name = 'dashboard/plans/plan_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, ' %s was deleted.'% self.get_object().name)
        return super(PlanDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('building_detail', kwargs={'pk': self.object.experiment.building.pk})


class PlanAddConnectionlView(LoginRequiredMixin, ContentUserOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        ConnectionFormSet = formset_factory(ConnectionForm)
        formset = ConnectionFormSet(request.POST)
        plan = get_object_or_404(Plan, pk=kwargs['pk'])
        if formset.is_valid():
            for form in formset:
                connection = form.save(commit=False)
                connection.plan = plan
                checkpoint = get_object_or_404(Checkpoint, pk=form.cleaned_data['checkpoint'])
                connection.checkpoint = checkpoint
                connection.save()
            messages.success(self.request, ' %s was saved.'% plan.name )
        return redirect(reverse_lazy('plan_detail', kwargs={'pk': kwargs['pk'], 'pk_experiment': kwargs['pk_experiment']}))


class PlanDeleteConnectionlView(LoginRequiredMixin, ContentUserOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        plan = get_object_or_404(Plan , pk=kwargs['pk'])
        plan.connection_set.all().delete()
        messages.success(self.request, ' %s was deleted.'% plan.name )
        return redirect(reverse_lazy('plan_detail', kwargs={'pk': kwargs['pk'], 'pk_experiment': kwargs['pk_experiment']}))

    def get(self, request, *args, **kwargs):
        plan = get_object_or_404(Plan, pk=kwargs['pk'])
        return render(request, 'dashboard/plans/connections_delete.html', {'plan':plan})

#JSON
class GetCheckpointsOfSpecificPlan(View):
    def get(self, request, *args, **kwargs):
        experiment = get_object_or_404(Experiment, pk=kwargs['pk_experiment'])
        plan = get_object_or_404(Plan, pk=kwargs['pk'])
        checkpoints = plan.connection_set.all()
        return JsonResponse(serializers.serialize('json', checkpoints), safe=False)
