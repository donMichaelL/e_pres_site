from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import BuildingForm, FloorForm
from .models import Building, Floor


# Create your views here.
class BuildingNewView(FormView):
    form_class = BuildingForm
    template_name = 'dashboard/new_building.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        building = form.save(commit=False)
        building.user = self.request.user
        building.save()
        return super(BuildingNewView, self).form_valid(form)


class BuildingDetailView(UpdateView, DetailView):
    template_name = 'dashboard/building_detail.html'
    form_class = BuildingForm
    model = Building


class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'dashboard/building_delete.html'
    success_url = reverse_lazy('homepage')


class FloorNewView(CreateView):
    model = Floor
    template_name = 'dashboard/new_floor.html'
    fields = ['name', 'number', 'blueprint', 'max_evacuation_time', 'stud_number']

    def get_success_url(self):
        return reverse_lazy('building_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def get_context_data(self, **kwargs):
        context = super(FloorNewView, self).get_context_data(**kwargs)
        context['building'] = self.kwargs.get(self.pk_url_kwarg)
        return context

    def form_valid(self, form):
        floor = form.save(commit=False)
        building = get_object_or_404(Building, pk= self.kwargs.get(self.pk_url_kwarg))
        floor.building = building
        floor.save()
        return super(FloorNewView, self).form_valid(form)


class FloorDetailView(UpdateView, DetailView):
    template_name = 'dashboard/floor_detail.html'
    form_class = FloorForm
    model = Floor

    def get_success_url(self):
        return self.object.get_building_url()


class FloorDeleteView(DeleteView):
    model = Floor
    template_name = 'dashboard/floor_delete.html'

    def get_success_url(self):
        return self.object.get_building_url()
