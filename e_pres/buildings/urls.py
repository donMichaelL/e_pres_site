from django.conf.urls import patterns, url
from .views import BuildingListView, BuildingNewView, BuildingDetailView, BuildingDeleteView, FloorNewView, FloorDetailView, FloorDeleteView
from questionnaires.views import PreparednessQuestionnaireView, PreparednessQuestionnaireNew

urlpatterns = [
    url(r'^$', BuildingListView.as_view(), name="building_list"),
    url(r'^(?P<pk>\d+)/$', BuildingDetailView.as_view(), name="building_detail"),
    url(r'^(?P<pk>\d+)/delete/$', BuildingDeleteView.as_view(), name="building_delete"),
    url(r'^new/$', BuildingNewView.as_view(), name="building_new"),
    url(r'^(?P<pk>\d+)/floor/new/$', FloorNewView.as_view(), name="floor_new"),
    url(r'^(?P<pk_building>\d+)/floor/(?P<pk>\d+)/$', FloorDetailView.as_view(), name="floor_detail"),
    url(r'^(?P<pk_building>\d+)/floor/(?P<pk>\d+)/delete/$', FloorDeleteView.as_view(), name="floor_delete"),

    url(r'^(?P<pk>\d+)/preparedness_questionnaire/$', PreparednessQuestionnaireView.as_view(), name="preparedness_questionnaire_list"),
    url(r'^(?P<pk>\d+)/preparedness_questionnaire/new/$', PreparednessQuestionnaireNew.as_view(), name="preparedness_questionnaire_new"),

]
