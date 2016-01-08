from django.shortcuts import render
from django.views.generic import View
from allauth.account.forms import LoginForm
from allauth.account.views import PasswordChangeView
from buildings.models import Building
from .forms import UserForm, UserProfileForm
# Create your views here.

class HomepageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            buildings = request.user.building_set.all()
            context = {'buildings': buildings}
            return render(request,'dashboard/buildings.html', context)
        else:
            form = LoginForm()
            context = {'form': form}
            return render(request, 'account/login.html', context)


class LoginAfterPasswordChangeView(PasswordChangeView):
    success_url = "/"


class ProfileFormView(View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=request.user.userprofile)
        context = {
            'user_form': user_form,
            'user_profile_form': user_profile_form
        }
        return render(request,'dashboard/profile.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST, instance=request.user)
        user_profile_form = UserProfileForm(data=request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
        context = {
                'user_form': user_form,
                'user_profile_form': user_profile_form
        }
        return render(request,'dashboard/profile.html', context)
