from django import forms
from tags.models import Tag
from .models import Plan, Connection

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        exclude = ['experiment']

    # def __init__(self, *args, **kwargs):
    #     super(PlanForm, self).__init__(*args, **kwargs)
    #     print self
    #     self.fields['tag_leader'].queryset = Tag.objects.filter(teacher__isnull=True)


class ConnectionForm(forms.ModelForm):
    checkpoint = forms.IntegerField()
    class Meta:
        model = Connection
        exclude = ['plan', 'checkpoint']
