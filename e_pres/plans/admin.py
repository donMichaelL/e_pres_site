from django.contrib import admin
from .models import Plan, Connection


class PlanAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'experiment_name' ,'disaster', 'owner']
    model = Plan

    def experiment_name(self, obj):
        return obj.experiment.name

    def disaster(self, obj):
        return obj.experiment.get_disaster_display()

    def owner(self, obj):
        return obj.experiment.user


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['experiment', '__unicode__', 'checkpoint', 'seq']
    model = Connection

    def experiment(self, obj):
        return obj.plan.experiment.name

admin.site.register(Plan, PlanAdmin)
admin.site.register(Connection, ConnectionAdmin)
