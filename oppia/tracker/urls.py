
# oppia/tracker/views.py
from django.conf.urls import include, url
from oppia.tracker import views as tracker_views

urlpatterns = [
    url(r'^upload/$', tracker_views.upload_view, name="oppia_tracker_upload"),
]