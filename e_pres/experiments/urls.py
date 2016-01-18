from django.conf.urls import patterns, url
from .views import ExperimentListView, ExperimentNewView, ExperimentDeleteView, ExperimentDetailView, CheckpointInsertView, CheckpointDeleteView
from plans.views import PlanNewView, PlanDetailView, PlanDeleteView, PlanAddConnectionlView

urlpatterns = [
    url(r'^$', ExperimentListView.as_view(), name="test_list"),
    url(r'^(?P<pk>\d+)/$', ExperimentDetailView.as_view(), name="test_detail"),
    url(r'^new/$', ExperimentNewView.as_view(), name="test_new"),
    url(r'^delete/(?P<pk>\d+)/$', ExperimentDeleteView.as_view(), name="test_delete"),
    url(r'^add_checkpoint/$', CheckpointInsertView.as_view(), name="checkpoint_new"),
    url(r'^delete_checkpoint/(?P<pk>\d+)/$', CheckpointDeleteView.as_view(), name="checkpoint_delete"),
    url(r'^(?P<pk>\d+)/plan/new/$', PlanNewView.as_view(), name="new_plan"),
        url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/$', PlanDetailView.as_view(), name="plan_detail"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/delete/$', PlanDeleteView.as_view(), name="plan_delete"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/add/connection/$', PlanAddConnectionlView.as_view(), name="plan_add_connection"),
]
