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
# Production
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from accounts.views import HomepageView, LoginAfterPasswordChangeView, ProfileFormView, LanguageChooserView
from tags.views import InitTagsView, AntennaStatusView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name="homepage"),
    url(r'^language-selector/$', LanguageChooserView.as_view(), name="language_selector"),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/$', ProfileFormView.as_view(), name="profile_settings"),
    url(r'^building/', include('buildings.urls')),
    url(r'^experiment/', include('experiments.urls')),
    url(r'^accounts/password/change/$', LoginAfterPasswordChangeView.as_view(), name='account_change_password'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^init-tags/', InitTagsView.as_view(), name="init_tags"),
    url(r'^antenna-status/', AntennaStatusView.as_view(), name="antenna-status"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)


# Production
# urlpatterns += staticfiles_urlpatterns()
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
