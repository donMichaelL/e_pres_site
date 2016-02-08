from django import  forms
from .models import Plan, Connection

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        exclude = ['experiment']

    # def __init__(self, *args, **kwargs):
    #     super(PlanForm, self).__init__(*args, **kwargs)
        #self.fields['before'].choices =


class ConnectionForm(forms.ModelForm):
    checkpoint = forms.IntegerField()
    class Meta:
        model = Connection
        exclude = ['plan', 'checkpoint']
