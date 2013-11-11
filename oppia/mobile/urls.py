# oppia/mobile/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^scorecard/$', 'oppia.mobile.views.scorecard_view', name="oppia_mobile_scorecard"),
    url(r'^monitor/$', 'oppia.mobile.views.monitor_home_view', name="oppia_monitor_home"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/recent/$', 'oppia.mobile.views.monitor_cohort_recent_view', name="oppia_monitor_cohort_recent"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/overall/$', 'oppia.mobile.views.monitor_cohort_overall_view', name="oppia_monitor_cohort_overall"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/quizzes/$', 'oppia.mobile.views.monitor_cohort_quizzes_view', name="oppia_monitor_cohort_quizzes"),
    url(r'^monitor/cohort/(?P<cohort_id>\d+)/student/(?P<student_id>\d+)$', 'oppia.mobile.views.monitor_cohort_student_view', name="oppia_monitor_cohort_student"),
    
    url(r'^course/(?P<course_id>\d+)/$', 'oppia.mobile.views.preview_course_home', name="oppia_preview_course_home"),
)
