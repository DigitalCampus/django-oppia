# oppia/viz/urls.py
from django.conf.urls import url

from viz import views as oppia_viz_views

urlpatterns = [
        url(r'^summary/$', oppia_viz_views.summary_view, name="oppia_viz_summary"),
        url(r'^map/$', oppia_viz_views.map_view, name="oppia_viz_map"),
        ]
