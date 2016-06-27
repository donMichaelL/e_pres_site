from django import forms
from django.forms.widgets import TextInput, DateInput
from buildings.models import Building
from .models import Experiment, Checkpoint


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        exclude = ['user', 'finished', 'in_progress', 'evacuation_time', 'starting_time']

    def __init__(self, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)
        self.fields['execution_date'].widget = DateInput(format=('%d-%m-%Y'), attrs={
            'id': 'datepicker'
            })
        self.fields['execution_time'].widget = TextInput(attrs={
            'id': 'timepicker'
            })
        self.fields['execution_date'].input_formats = ['%d-%m-%Y']


class CheckpointForm(forms.ModelForm):
    pk = forms.IntegerField(required=False)
    class Meta:
        model = Checkpoint
        fields = '__all__'
