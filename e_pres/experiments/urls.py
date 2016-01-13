from django.conf.urls import patterns, url
from .views import ExperimentListView, ExperimentNewView, ExperimentDeleteView, ExperimentDetailView

urlpatterns = [
    url(r'^$', ExperimentListView.as_view(), name="test_list"),
    url(r'^(?P<pk>\d+)$', ExperimentDetailView.as_view(), name="test_detail"),
    url(r'^new/$', ExperimentNewView.as_view(), name="test_new"),
    url(r'^delete/(?P<pk>\d+)$', ExperimentDeleteView.as_view(), name="test_delete"),

]
