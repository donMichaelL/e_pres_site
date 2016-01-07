from django.shortcuts import render
from django.views.generic import View
from allauth.account.forms import LoginForm
# Create your views here.

class HomepageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            print 'Hello'
        else:
            form = LoginForm()
            context = {'form': form}
            return render(request, 'account/login.html', context)
