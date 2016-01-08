from django import forms
from .models import Building


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        exclude = ['user']
