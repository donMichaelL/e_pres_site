from django.conf.urls import patterns, url
from .views import ExperimentListView, ExperimentNewView, ExperimentDeleteView, ExperimentDetailView, CheckpointInsertView, CheckpointDeleteView
from plans.views import PlanNewView, PlanDetailView, PlanDeleteView, PlanAddConnectionlView, PlanDeleteConnectionlView
from analytics.views import PostExperiment, ReportFluxPostExperiment

urlpatterns = [
    url(r'^$', ExperimentListView.as_view(), name="experiment_list"),
    url(r'^new/$', ExperimentNewView.as_view(), name="experiment_new"),
    url(r'^(?P<pk>\d+)/$', ExperimentDetailView.as_view(), name="experiment_detail"),
    url(r'^(?P<pk>\d+)/post-execution$', PostExperiment.as_view(), name="post_experiment"),
    url(r'^(?P<pk>\d+)/delete/$', ExperimentDeleteView.as_view(), name="experiment_delete"),
    url(r'^(?P<pk>\d+)/add_checkpoint/$', CheckpointInsertView.as_view(), name="checkpoint_new"),
    url(r'^(?P<pk_experiment>\d+)/post-execution/(?P<pk>\d+)$', ReportFluxPostExperiment.as_view(), name="report_flux_post_experiment"),
    url(r'^(?P<pk_experiment>\d+)/checkpoint/(?P<pk>\d+)/delete/$', CheckpointDeleteView.as_view(), name="checkpoint_delete"),
    url(r'^(?P<pk_experiment>\d+)/plan/new/$', PlanNewView.as_view(), name="new_plan"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/$', PlanDetailView.as_view(), name="plan_detail"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/delete/$', PlanDeleteView.as_view(), name="plan_delete"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/add/connection/$', PlanAddConnectionlView.as_view(), name="plan_add_connection"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/delete/connections/$', PlanDeleteConnectionlView.as_view(), name="plan_delete_connections"),
]
