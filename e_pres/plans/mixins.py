from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from experiments.models import Experiment


class ContentUserOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        print kwargs
        experiment =  get_object_or_404(Experiment, pk=kwargs['pk_experiment'])
        if experiment.user == request.user:
            return super(ContentUserOnlyMixin, self).dispatch( request, *args, **kwargs)
        else:
            raise PermissionDenied()
            
