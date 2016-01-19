from django import forms
from buildings.models import Building
from .models import Experiment, Checkpoint


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        exclude = ['user']

class CheckpointForm(forms.ModelForm):
    pk = forms.IntegerField(required=False)
    class Meta:
        model = Checkpoint
        fields = '__all__'
