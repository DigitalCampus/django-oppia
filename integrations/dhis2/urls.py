# oppia/reports/urls.py
from django.conf.urls import url

from integrations.dhis2 import views as oppia_dhis2_views

urlpatterns = [
        url(r'^/$', oppia_dhis2_views.dhis2, name="oppia_integrations_dhis2")
        ]
