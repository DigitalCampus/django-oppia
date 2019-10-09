# integrations/xapi/urls.py
from django.conf.urls import url
from django.views.generic import TemplateView

from integrations.xapi import views as xapi_views

urlpatterns = [
        url(r'^export/$', xapi_views.csv_export, name="oppia_xapi_csv_export"),
]