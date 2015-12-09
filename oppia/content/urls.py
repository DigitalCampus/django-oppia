# oppia/content/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
                url(r'^video-embed-helper/$', 'oppia.content.views.video_embed_helper', name="oppia_video_embed_helper"),
              )      