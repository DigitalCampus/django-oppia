# oppia/av/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
   url(r'^upload/$', 'oppia.av.views.upload_view', name="oppia_av_upload"),
)
