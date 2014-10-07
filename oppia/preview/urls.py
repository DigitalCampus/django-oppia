# oppia/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',

    url(r'^$', 'oppia.preview.views.home_view', name="oppia_preview_home"),
    url(r'^(?P<id>\d+)/$', 'oppia.preview.views.course_home_view', name="oppia_preview_course_home"),
    url(r'^(?P<course_id>\d+)/(?P<activity_id>\d+)/$', 'oppia.preview.views.course_activity_view', name="oppia_preview_course_activity"),
    
)
