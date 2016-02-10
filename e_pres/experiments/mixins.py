from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class ContentUserOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.building.user == request.user or request.user.is_superuser:
            return super(ContentUserOnlyMixin, self).dispatch( request, *args, **kwargs)
        else:
            raise PermissionDenied()


class CheckpointContentUserOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.experiment.building.user == request.user or request.user.is_superuser:
            return super(CheckpointContentUserOnlyMixin, self).dispatch( request, *args, **kwargs)
        else:
            raise PermissionDenied()
