# oppia/urls.py
from django.conf.urls import url

from oppia.preview import views as oppia_preview_views

urlpatterns = [
    url(r'^$', oppia_preview_views.home_view, name="oppia_preview_home"),
    url(r'^(?P<id>\d+)/$', oppia_preview_views.course_home_view, name="oppia_preview_course_home"),
    url(r'^(?P<course_id>\d+)/(?P<activity_id>\d+)/$', oppia_preview_views.course_activity_view, name="oppia_preview_course_activity"),
]
