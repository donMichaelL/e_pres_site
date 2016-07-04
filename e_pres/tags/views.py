from django.shortcuts import render
from django.views.generic import View


class InitTagsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/init_tags.html', {})

    def post(self, request, *args, **kwargs):
        pass
