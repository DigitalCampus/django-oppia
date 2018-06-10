# oppia/deviceadmin/urls.py
from django.conf.urls import url

from oppia.deviceadmin import views as oppia_deviceadmin_views
urlpatterns = [
    url(r'^list/$', oppia_deviceadmin_views.user_devices_list, name="deviceadmin_devices_list"),
    url(r'^list/send_message$', oppia_deviceadmin_views.send_message_to_device, name="deviceadmin_send_message"),
]
