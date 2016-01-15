from django.contrib import admin
from .models import Experiment, Checkpoint


class ExperimentAdmin(admin.ModelAdmin):
    model = Experiment
    list_display = ['__unicode__', 'disaster' ,'building_name', 'owner' ]

    def building_name(self, obj):
        return obj.building

    def owner(self, obj):
        return obj.building.user

admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Checkpoint)
