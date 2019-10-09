# oppia/reports/urls.py
from django.conf.urls import url

from integrations.dhis import views as oppia_dhis_views

urlpatterns = [
        url(r'^export/$', oppia_dhis_views.export, name="oppia_integrations_dhis_export")
        ]
