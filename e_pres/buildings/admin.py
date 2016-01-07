from django.contrib import admin
from .models import Building

class BuildingAdmin(admin.ModelAdmin):
    model = Building
    list_display = ['name', 'owner']

    def owner(self, obj):
        return obj



admin.site.register(Building, BuildingAdmin)
