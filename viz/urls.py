# oppia/viz/urls.py
from django.conf.urls import url

from viz import views as oppia_viz_views

urlpatterns = [
        url(r'^summary/$',
            oppia_viz_views.Summary.as_view(),
            name="oppia_viz_summary"),
        url(r'^map/$', oppia_viz_views.Map.as_view(), name="oppia_viz_map"),
        ]
