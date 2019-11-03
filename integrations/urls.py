# oppia/reports/urls.py
from django.conf.urls import include, url

from integrations import views as oppia_integrations_views

urlpatterns = [
        url(r'^$', oppia_integrations_views.home,
            name="oppia_integrations_home"),
        url(r'^dhis/', include('integrations.dhis.urls')),
        url(r'^xapi/', include('integrations.xapi.urls')),
        ]
