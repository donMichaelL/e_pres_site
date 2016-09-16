from django.contrib import admin
from .models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'teacher' ,'user', 'sequence']

admin.site.register(Tag, TagAdmin)
