from django import  forms
from .models import Plan, Connection

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        exclude = ['experiment']


class ConnectionForm(forms.ModelForm):
    checkpoint = forms.IntegerField()
    class Meta:
        model = Connection
        exclude = ['plan', 'checkpoint']
