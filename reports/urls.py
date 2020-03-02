# oppia/reports/urls.py
from django.conf.urls import url

from reports import views as oppia_reports_views

urlpatterns = [
        url(r'^completion_rates/$',
            oppia_reports_views.CompletionRates.as_view(),
            name="oppia_completion_rates"),
        url(r'^completion_rates/(?P<course_id>\d+)/$',
            oppia_reports_views.CourseCompletionRates.as_view(),
            name="course_completion_rates"),
        ]
