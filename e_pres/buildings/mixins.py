from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class ContentUserOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user:
            return super(ContentUserOnlyMixin, self).dispatch( request, *args, **kwargs)
        else:
            raise PermissionDenied()


class FloorContentUserOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.building.user == request.user:
            return super(FloorContentUserOnlyMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()


class CheckpointContentUserOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.experiment.user == request.user:
            return super(CheckpointContentUserOnlyMixin, self).dispatch( request, *args, **kwargs)
        else:
            raise PermissionDenied()
