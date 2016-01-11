from django import forms
from .models import Building, Floor


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        exclude = ['user']


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        exclude = ['building']
