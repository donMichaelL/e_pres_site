from django.conf.urls import patterns, url
from .views import ExperimentListView, ExperimentNewView, ExperimentDeleteView, ExperimentDetailView, CheckpointInsertView, CheckpointDeleteView, ExperimentStartView, ExperimentStopView
from plans.views import PlanNewView, PlanDetailView, PlanDeleteView, PlanAddConnectionlView, PlanDeleteConnectionlView, GetCheckpointsOfSpecificPlan
from analytics.views import PostExperiment, ReportFluxPostExperiment, RealTimeView
from questionnaires.views import EvaluationQuestionnaireView, EvaluationQuestionnaireNew, EvaluationStudentsQuestionnaireView, EvaluationTeachersQuestionnaireNew


urlpatterns = [
    url(r'^$', ExperimentListView.as_view(), name="experiment_list"),
    url(r'^new/$', ExperimentNewView.as_view(), name="experiment_new"),
    url(r'^(?P<pk>\d+)/$', ExperimentDetailView.as_view(), name="experiment_detail"),

    url(r'^(?P<pk>\d+)/start/$', ExperimentStartView.as_view(), name="start_experiment"),
    url(r'^(?P<pk>\d+)/stop/$', ExperimentStopView.as_view(), name="stop_experiment"),



    url(r'^(?P<pk>\d+)/post-execution/$', PostExperiment.as_view(), name="post_experiment"),
    url(r'^(?P<pk>\d+)/realtime/$', RealTimeView.as_view(), name="realtime"),
    url(r'^(?P<pk>\d+)/delete/$', ExperimentDeleteView.as_view(), name="experiment_delete"),
    url(r'^(?P<pk>\d+)/add_checkpoint/$', CheckpointInsertView.as_view(), name="checkpoint_new"),
    url(r'^(?P<pk_experiment>\d+)/post-execution/(?P<pk>\d+)$', ReportFluxPostExperiment.as_view(), name="report_flux_post_experiment"),
    url(r'^(?P<pk_experiment>\d+)/checkpoint/(?P<pk>\d+)/delete/$', CheckpointDeleteView.as_view(), name="checkpoint_delete"),
    url(r'^(?P<pk_experiment>\d+)/plan/new/$', PlanNewView.as_view(), name="new_plan"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/api/$', GetCheckpointsOfSpecificPlan.as_view(), name="get_checkpoints_of_plan"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/$', PlanDetailView.as_view(), name="plan_detail"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/delete/$', PlanDeleteView.as_view(), name="plan_delete"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/add/connection/$', PlanAddConnectionlView.as_view(), name="plan_add_connection"),
    url(r'^(?P<pk_experiment>\d+)/plan/(?P<pk>\d+)/delete/connections/$', PlanDeleteConnectionlView.as_view(), name="plan_delete_connections"),

    url(r'^(?P<pk>\d+)/evacuation_questionnaire/$', EvaluationQuestionnaireView.as_view(), name="evacuation_questionnaire_list"),
    url(r'^(?P<pk>\d+)/evacuation_questionnaire/new/$', EvaluationQuestionnaireNew.as_view(), name="evacuation_questionnaire_new"),

    url(r'^(?P<pk>\d+)/student_questionnaire/$', EvaluationStudentsQuestionnaireView.as_view(), name="student_questionnaire_list"),
    url(r'^(?P<pk>\d+)/teacher_questionnaire/new/$', EvaluationTeachersQuestionnaireNew.as_view(), name="teachers_questionnaire_list"),
]
