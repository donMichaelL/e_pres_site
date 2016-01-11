from django.contrib import admin
from.models import Test


class TestAdmin(admin.ModelAdmin):
    model = Test
    list_display = ['__unicode__', 'disaster' ,'building_name', 'owner' ]

    def building_name(self, obj):
        return obj.building

    def owner(self, obj):
        return obj.building.user

admin.site.register(Test, TestAdmin)
