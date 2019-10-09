# oppia/reports/urls.py
from django.conf.urls import include, url

from integrations import views as oppia_integrations_views

urlpatterns = [
        url(r'^$', oppia_integrations_views.integrations, name="oppia_integrations"),
        url(r'^dhis/', include('integrations.dhis.urls')),
        #url(r'^xapi/', include('xapi.urls')),
        ]


