from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['__unicode__', 'first_name', 'last_name', 'organization','email', 'phone_number']

    def first_name(self,obj):
        return obj.user.first_name

    def last_name(self,obj):
        return obj.user.last_name

    def email(self,obj):
        return obj.user.email





admin.site.register(UserProfile, UserProfileAdmin)
