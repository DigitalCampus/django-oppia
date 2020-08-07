from django.urls import path
from quiz import views


app_name = 'quiz'
urlpatterns = [

    path('<int:course_id>/feedback/<int:feedback_id>/download',
         views.FeedbackDownload.as_view(),
         name="feedback_results_download"),

    path('<int:course_id>/quiz/<int:quiz_id>/download',
         views.QuizDownload.as_view(),
         name="quiz_results_download")
    ]
