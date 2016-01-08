from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .forms import BuildingForm
from .models import Building


# Create your views here.
class NewBuildingView(FormView):
    form_class = BuildingForm
    template_name = 'dashboard/new_building.html'
    success_url = '/'

    def form_valid(self, form):
        building = form.save(commit=False)
        building.user = self.request.user
        building.save()
        return super(NewBuildingView, self).form_valid(form)


class BuildingDetailView(UpdateView, DetailView):
    template_name = 'dashboard/building_detail.html'
    form_class = BuildingForm
    model = Building
