# oppia/deviceadmin/urls.py

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^list/$', 'oppia.deviceadmin.views.user_devices_list', name="deviceadmin_devices_list"),
    url(r'^list/send_message$', 'oppia.deviceadmin.views.send_message_to_device', name="deviceadmin_send_message"),
)