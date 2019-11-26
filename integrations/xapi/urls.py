# integrations/xapi/urls.py
from django.conf.urls import url

from integrations.xapi import views as xapi_views

urlpatterns = [
        url(r'^$', xapi_views.home, name="oppia_integrations_xapi_home"),
        url(r'^export/$',
            xapi_views.csv_export,
            name="oppia_integrations_xapi_csv_export"),
]
