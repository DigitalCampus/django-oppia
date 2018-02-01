# oppia/av/urls.py
from django.conf.urls import url

from oppia.av import views as oppia_av_views

urlpatterns = [
   url(r'^$', oppia_av_views.home_view, name="oppia_av_home"),
   url(r'^upload/$', oppia_av_views.upload_view, name="oppia_av_upload"),
   url(r'^upload/success/(?P<id>\d+)$', oppia_av_views.upload_success_view, name="oppia_av_upload_success"),
]