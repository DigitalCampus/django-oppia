
# oppia/activitylog/views.py
from django.conf.urls import url
from django.views.generic import TemplateView

from activitylog import views as activitylog_views

urlpatterns = [
    url(r'^upload/$', activitylog_views.upload_view, name="oppia_activitylog_upload"),
    url(r'^upload/success/$', TemplateView.as_view(template_name="oppia/activitylog/upload_success.html"), name="oppia_activitylog_upload_success"),
]
