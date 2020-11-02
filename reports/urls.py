from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('completion_rates/',
         views.CompletionRates.as_view(),
         name="completion_rates"),
    path('completion_rates/<int:course_id>/',
         views.CourseCompletionRates.as_view(),
         name="course_completion_rates"),
]
