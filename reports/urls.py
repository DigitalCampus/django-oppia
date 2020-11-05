from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('',
         views.HomeView.as_view(),
         name="index"),
    path('completion_rates',
         views.CompletionRates.as_view(),
         name="completion_rates"),
    path('completion_rates/<int:course_id>',
         views.CourseCompletionRates.as_view(),
         name="course_completion_rates"),
    path('unique_users',
         views.UniqueUsers.as_view(),
         name="unique_users"),
    path('daus',
         views.DailyActiveUsers.as_view(),
         name="daus"),
]
