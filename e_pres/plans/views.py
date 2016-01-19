from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.forms import formset_factory
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from experiments.models import Experiment, Checkpoint
from .models import Plan, Connection
from .forms import PlanForm, ConnectionForm


class PlanNewView(CreateView):
    model = Plan
    template_name = 'dashboard/plans/new_plan.html'
    fields = ['name']

    def get_success_url(self):
        return reverse_lazy('test_list')

    def get_context_data(self, **kwargs):
        context = super(PlanNewView, self).get_context_data(**kwargs)
        context['test'] = self.kwargs.get(self.pk_url_kwarg)
        return context

    def form_valid(self, form):
        plan = form.save(commit=False)
        experiment = get_object_or_404(Experiment, pk= self.kwargs.get(self.pk_url_kwarg))
        plan.experiment = experiment
        plan.save()
        messages.success(self.request, ' %s was created.'% plan.name )
        return super(PlanNewView, self).form_valid(form)


class PlanDetailView(UpdateView, DetailView):
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
        return context


class PlanDeleteView(DeleteView):
    model = Plan
    template_name = 'dashboard/plans/plan_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, ' %s was deleted.'% self.get_object().name )
        return super(PlanDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('test_list')


class PlanAddConnectionlView(View):
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

class PlanDeleteConnectionlView(View):
    def post(self, request, *args, **kwargs):
        plan = get_object_or_404(Plan , pk=kwargs['pk'])
        plan.connection_set.all().delete()
        messages.success(self.request, ' %s was deleted.'% plan.name )
        return redirect(reverse_lazy('plan_detail', kwargs={'pk': kwargs['pk'], 'pk_experiment': kwargs['pk_experiment']}))

    def get(self, request, *args, **kwargs):
        plan = get_object_or_404(Plan, pk=kwargs['pk'])
        return render(request, 'dashboard/plans/connections_delete.html', {'plan':plan})
