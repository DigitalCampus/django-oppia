# oppia/deviceadmin/urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^list/$', 'oppia.deviceadmin.views.user_devices_list', name="deviceadmin_devices_list"),
)