from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import FormView
from .models import Experiment
from .forms import ExperimentForm

class ExperimentListView(ListView):
    model = Experiment
    template_name = 'dashboard/experiments/list_tests.html'

    def get_queryset(self):
        return Experiment.objects.filter(user=self.request.user)


class ExperimentNewView(FormView):
    form_class = ExperimentForm
    template_name = 'dashboard/experiments/new_test.html'
    #success_url = reverse_lazy('test_list')

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
