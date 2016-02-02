from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from experiments.models import return_choices
from .forms import BuildingForm, FloorForm
from .models import Building, Floor
from .mixins import ContentUserOnlyMixin, FloorContentUserOnlyMixin
from django.core.exceptions import PermissionDenied


class BuildingListView(LoginRequiredMixin, ListView):
    model = Building
    template_name = 'dashboard/buildings/list_building.html'

    def get_queryset(self):
        return Building.objects.filter(user=self.request.user)


class BuildingNewView(LoginRequiredMixin, FormView):
    form_class = BuildingForm
    template_name = 'dashboard/buildings/new_building.html'
    success_url = reverse_lazy('building_list')

    def form_valid(self, form):
        building = form.save(commit=False)
        building.user = self.request.user
        building.save()
        messages.success(self.request, ' %s was created.'% building.name )
        return super(BuildingNewView, self).form_valid(form)


class BuildingDetailView(LoginRequiredMixin, ContentUserOnlyMixin, UpdateView, DetailView):
    template_name = 'dashboard/buildings/building_detail.html'
    form_class = BuildingForm
    model = Building

    def form_valid(self, form):
        messages.success(self.request, ' %s was updated.'% form.cleaned_data['name'] )
        return super(BuildingDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BuildingDetailView, self).get_context_data(**kwargs)
        context['disaster_choices'] = return_choices()
        return context


class BuildingDeleteView(LoginRequiredMixin, ContentUserOnlyMixin, DeleteView):
    model = Building
    template_name = 'dashboard/buildings/building_delete.html'
    success_url = reverse_lazy('building_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, ' %s was deleted.'% self.get_object().name )
        return super(BuildingDeleteView, self).delete(request, *args, **kwargs)


class FloorNewView(LoginRequiredMixin, CreateView):
    model = Floor
    template_name = 'dashboard/floors/new_floor.html'
    fields = ['name', 'number', 'blueprint', 'max_evacuation_time', 'stud_number']

    def get_success_url(self):
        return reverse_lazy('building_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def get_context_data(self, **kwargs):
        context = super(FloorNewView, self).get_context_data(**kwargs)
        building_id = self.kwargs.get(self.pk_url_kwarg)
        context['building'] = building_id
        building = get_object_or_404(Building, pk=building_id)
        if building.user != self.request.user:
            raise PermissionDenied()
        return context

    def form_valid(self, form):
        floor = form.save(commit=False)
        building = get_object_or_404(Building, pk= self.kwargs.get(self.pk_url_kwarg))
        floor.building = building
        floor.save()
        messages.success(self.request, ' %s was created.'% floor.name )
        return super(FloorNewView, self).form_valid(form)


class FloorDetailView(LoginRequiredMixin, FloorContentUserOnlyMixin, UpdateView, DetailView):
    template_name = 'dashboard/floors/floor_detail.html'
    form_class = FloorForm
    model = Floor

    def get_success_url(self):
        return self.object.get_building_url()

    def form_valid(self, form):
        messages.success(self.request, ' %s was updated.'% form.cleaned_data['name'] )
        return super(FloorDetailView, self).form_valid(form)


class FloorDeleteView(LoginRequiredMixin, FloorContentUserOnlyMixin, DeleteView):
    model = Floor
    template_name = 'dashboard/floors/floor_delete.html'

    def get_success_url(self):
        return self.object.get_building_url()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, ' %s was deleted.'% self.get_object().name )
        return super(FloorDeleteView, self).delete(request, *args, **kwargs)
