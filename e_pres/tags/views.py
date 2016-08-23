from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .models import Tag

from django.core import serializers
import json

class AntennaStatusView(TemplateView):
    template_name = 'dashboard/antenna-status.html'

class InitTagsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            teachers = Tag.objects.filter(teacher__isnull=True).filter(user=request.user)
            tags = [tag.encode("utf8") for tag in Tag.objects.filter(user=request.user).values_list('tag_string', flat=True)]
            return render(request, 'dashboard/init_tags.html', {'teachers': teachers, 'tags': tags})
        raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
            tag = self.request.POST.get('tag', '')
            teacher = self.request.POST.get('teacher', '')
            if teacher and teacher != tag:
                teacher_tag = Tag.objects.get(tag_string=teacher)
                Tag.objects.get_or_create(tag_string=tag, teacher=teacher_tag, user=user)
            else:
                Tag.objects.get_or_create(tag_string=tag, user=user)
            return JsonResponse('ok', status=201, safe=False)
        return JsonResponse('PermissionDenied',status=403, safe=False)

    def delete(self, request, *args, **kwargs):
        teacher = get_object_or_404(Tag, tag_string=request.GET.get('tag'))
        if request.user.is_authenticated():
            tags_queryset = Tag.objects.filter(user=request.user, teacher=teacher)
            tags_to_delete = [tag.encode("utf8") for tag in tags_queryset.values_list('tag_string', flat=True)]
            Tag.objects.filter(user=request.user, teacher=teacher).delete()
            teacher.delete()
            return JsonResponse(tags_to_delete, status=201, safe=False)
        return JsonResponse('PermissionDenied',status=403, safe=False)
