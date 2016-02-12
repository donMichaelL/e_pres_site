from django.contrib import admin
from .models import CheckpointReport
# Register your models here.

class CheckpointReportAdmin(admin.ModelAdmin):
    model = CheckpointReport
    list_display = ['__unicode__', 'checkpoint_pk', 'current_flux', 'max_flux', 'fail']

    def checkpoint_pk(self, obj):
        return obj.checkpoint.pk

    def max_flux(self, obj):
        return obj.checkpoint.flux

admin.site.register(CheckpointReport, CheckpointReportAdmin)
