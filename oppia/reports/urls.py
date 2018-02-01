# oppia/reports/urls.py
from django.conf.urls import url

from oppia.reports import views as oppia_reports_views

urlpatterns = [
        url(r'^completion_rates/$', oppia_reports_views.completion_rates, name="oppia_completion_rates"),
        url(r'^completion_rates/(?P<course_id>\d+)/$', oppia_reports_views.course_completion_rates, name="course_completion_rates"),
        ]
