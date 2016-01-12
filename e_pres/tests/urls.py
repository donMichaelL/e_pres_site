from django.conf.urls import patterns, url
from .views import TestListView, TestNewView, TestDeleteView

urlpatterns = [
    url(r'^$', TestListView.as_view(), name="test_list"),
    url(r'^new/$', TestNewView.as_view(), name="test_new"),
    url(r'^delete/(?P<pk>\d+)$', TestDeleteView.as_view(), name="test_delete"),

]
