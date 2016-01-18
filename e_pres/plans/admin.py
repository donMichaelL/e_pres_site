from django.contrib import admin
from .models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'experiment_name' ,'disaster', 'owner']
    model = Plan

    def experiment_name(self, obj):
        return obj.experiment.name

    def disaster(self, obj):
        return obj.experiment.get_disaster_display()

    def owner(self, obj):
        return obj.experiment.user


admin.site.register(Plan, PlanAdmin)
