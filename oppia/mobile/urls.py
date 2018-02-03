# oppia/mobile/urls.py
from django.conf.urls import url

from oppia.mobile import views as oppia_mobile_views

urlpatterns = [
    url(r'^scorecard/$',oppia_mobile_views.scorecard_view, name="oppia_mobile_scorecard"),
    url(r'^monitor/$', oppia_mobile_views.monitor_home_view, name="oppia_monitor_home"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/(?P<course_id>\d+)/progress/$', oppia_mobile_views.monitor_cohort_progress_view, name="oppia_monitor_cohort_progress"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/(?P<course_id>\d+)/quizzes/$', oppia_mobile_views.monitor_cohort_quizzes_view, name="oppia_monitor_cohort_quizzes"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/(?P<course_id>\d+)/media/$', oppia_mobile_views.monitor_cohort_media_view, name="oppia_monitor_cohort_media"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/student/(?P<student_id>\d+)$', oppia_mobile_views.monitor_cohort_student_view, name="oppia_monitor_cohort_student"),
]
