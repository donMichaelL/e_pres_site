"""e_pres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf.urls.static import static
from accounts.views import HomepageView, LoginAfterPasswordChangeView, ProfileFormView
from buildings.views import BuildingNewView, BuildingDetailView, BuildingDeleteView, FloorNewView, FloorDetailView, FloorDeleteView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name="homepage"),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/$', ProfileFormView.as_view(), name="profile_settings"),
    url(r'^building/(?P<pk>\d+)$', BuildingDetailView.as_view(), name="building_detail"),
    url(r'^building/delete/(?P<pk>\d+)$', BuildingDeleteView.as_view(), name="building_delete"),
    url(r'^building/new/$', BuildingNewView.as_view(), name="building_new"),
    url(r'^building/(?P<pk>\d+)/floor/new/$', FloorNewView.as_view(), name="floor_new"),
    url(r'^building/(?P<pk_building>\d+)/floor/(?P<pk>\d+)/$', FloorDetailView.as_view(), name="floor_detail"),
    url(r'^building/(?P<pk_building>\d+)/floor/(?P<pk>\d+)/delete/$', FloorDeleteView.as_view(), name="floor_delete"),
    url(r'^accounts/password/change/$', LoginAfterPasswordChangeView.as_view(), name='account_change_password'),
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += patterns('',) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += patterns('',) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
