# oppia/av/urls.py
from django.conf.urls import url

from av import views as oppia_av_views

urlpatterns = [
   url(r'^$', oppia_av_views.home_view, name="oppia_av_home"),
   url(r'^view/(?P<id>\d+)$', oppia_av_views.media_view, name="oppia_av_view"),
   url(r'^view/set-image-default/(?P<image_id>\d+)$', oppia_av_views.set_default_image_view, name="oppia_av_set_default_image"),
   
   url(r'^upload/$', oppia_av_views.upload_view, name="oppia_av_upload"),
   url(r'^upload/success/(?P<id>\d+)$', oppia_av_views.upload_success_view, name="oppia_av_upload_success"),
]
