# oppia/viz/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
        url(r'^summary/$', 'oppia.viz.views.summary_view', name="oppia_viz_summary"),
        url(r'^map/$', 'oppia.viz.views.map_view', name="oppia_viz_map"),
        )