from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import View
from django.contrib import messages
from django.utils.translation import LANGUAGE_SESSION_KEY
from allauth.account.forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordChangeView, LoginView
from django.http import JsonResponse
from buildings.models import Building
from .forms import UserForm, UserProfileForm


class HomepageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            buildings = request.user.building_set.all()
            context = {'object_list': buildings}
            return render(request,'dashboard/buildings/list_building.html', context)
        else:
            form = LoginForm()
            context = {'form': form}
            return render(request, 'account/login.html', context)


class LoginAfterPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = "/"


class ProfileFormView(LoginRequiredMixin, View):
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
            messages.success(request, ' %s profile was updated.'% self.request.user)
            return redirect(reverse('profile_settings'))
        context = {
                'user_form': user_form,
                'user_profile_form': user_profile_form
        }
        return render(request,'dashboard/profile.html', context)


class LanguageChooserView(View):
    def post(self, request, *args, **kwargs):
        language = request.POST.get('language')
        if language == 'el':
            request.session[LANGUAGE_SESSION_KEY] = 'el'
        else:
            request.session[LANGUAGE_SESSION_KEY] = 'en'
        return JsonResponse('ok', status=200, safe=False)
