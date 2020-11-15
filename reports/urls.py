from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('',
         views.HomeView.as_view(),
         name="index"),
    path('user-registrations',
         views.UserRegistrationsView.as_view(),
         name="user_registrations"),
    path('completion-rates',
         views.CompletionRatesView.as_view(),
         name="completion_rates"),
    path('completion-rates/<int:course_id>',
         views.CourseCompletionRatesView.as_view(),
         name="course_completion_rates"),
    path('unique-users',
         views.UniqueUsersView.as_view(),
         name="unique_users"),
    path('daily-active-users',
         views.DailyActiveUsersView.as_view(),
         name="daus"),
    path('monthly-active-users',
         views.MonthlyActiveUsersView.as_view(),
         name="maus"),
    path('total-time-spent',
         views.TotalTimeSpentView.as_view(),
         name="totaltimespent"),
    path('average-time-spent',
         views.AverageTimeSpentView.as_view(),
         name="averagetimespent"),
]
