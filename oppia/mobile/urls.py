# oppia/mobile/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^scorecard/$', 'oppia.mobile.views.scorecard_view', name="oppia_mobile_scorecard"),
)
