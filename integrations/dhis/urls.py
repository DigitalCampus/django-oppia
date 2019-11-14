# oppia/reports/urls.py
from django.conf.urls import url

from integrations.dhis import views as oppia_dhis_views

urlpatterns = [
        url(r'^$', oppia_dhis_views.home, name="oppia_integrations_dhis_home"),
        url(r'^export/latest/$',
            oppia_dhis_views.export_latest,
            name="oppia_integrations_dhis_export_latest"),
        url(r'^export/(?P<year>\d+)/(?P<month>\d+)$',
            oppia_dhis_views.export_month,
            name="oppia_integrations_dhis_export_month")
        ]
