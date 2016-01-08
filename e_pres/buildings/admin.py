from django.contrib import admin
from .models import Building, Floor

class BuildingAdmin(admin.ModelAdmin):
    model = Building
    list_display = ['name', 'owner']

    def owner(self, obj):
        return obj.user

class FloorAdmin(admin.ModelAdmin):
    model = Floor
    list_display= ['__unicode__', 'number','building_name', 'owner']

    def building_name(self, obj):
        return obj.building

    def owner(self, obj):
        return obj.building.user

admin.site.register(Building, BuildingAdmin)
admin.site.register(Floor, FloorAdmin)
