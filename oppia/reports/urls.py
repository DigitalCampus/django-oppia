# oppia/reports/urls.py
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
        url(r'^completion_rates/$', 'oppia.reports.views.completion_rates', name="oppia_completion_rates"),
        url(r'^completion_rates/(?P<course_id>\d+)/$', 'oppia.reports.views.course_completion_rates', name="course_completion_rates"),
        )
