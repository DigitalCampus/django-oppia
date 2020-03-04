from django.urls import path
from reports import views as oppia_reports_views

app_name = 'reports'

urlpatterns = [
    path('completion_rates/',
         oppia_reports_views.CompletionRates.as_view(),
         name="completion_rates"),
    path('completion_rates/<int:course_id>/',
         oppia_reports_views.CourseCompletionRates.as_view(),
         name="course_completion_rates"),
]
