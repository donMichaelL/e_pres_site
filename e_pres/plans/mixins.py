from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from experiments.models import Experiment


class ContentUserOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        experiment =  get_object_or_404(Experiment, pk=kwargs['pk_experiment'])
        if experiment.building.user == request.user or request.user.is_superuser:
            return super(ContentUserOnlyMixin, self).dispatch( request, *args, **kwargs)
        else:
            raise PermissionDenied()
