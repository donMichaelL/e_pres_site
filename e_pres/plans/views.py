from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from experiments.models import Experiment
from .models import Plan
from .forms import PlanForm


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
        return super(PlanNewView, self).form_valid(form)


class PlanDetailView(UpdateView, DetailView):
    template_name = 'dashboard/plans/plan_detail.html'
    form_class = PlanForm
    model = Plan

    def get_success_url(self):
        return self.object.get_absolute_url()


class PlanDeleteView(DeleteView):
    model = Plan
    template_name = 'dashboard/plans/plan_delete.html'

    def get_success_url(self):
        return reverse_lazy('test_list')
