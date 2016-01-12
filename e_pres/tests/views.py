from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import FormView
from .models import Test
from .forms import TestForm

class TestListView(ListView):
    model = Test
    template_name = 'dashboard/experiments/list_tests.html'

    def get_queryset(self):
        return Test.objects.filter(user=self.request.user)


class TestNewView(FormView):
    form_class = TestForm
    template_name = 'dashboard/experiments/new_test.html'
    success_url = reverse_lazy('test_list')

    def form_valid(self, form):
        test = form.save(commit=False)
        test.user = self.request.user
        test.save()
        return super(TestNewView, self).form_valid(form)


class TestDeleteView(DeleteView):
    model = Test
    template_name = 'dashboard/experiments/test_delete.html'
    success_url = reverse_lazy('test_list')
