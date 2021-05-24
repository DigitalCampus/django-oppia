from django.urls import path
from quiz import views


app_name = 'quiz'
urlpatterns = [

    path('<int:course_id>/feedback/<int:feedback_id>/download', views.feedback_download, name="feedback_results_download"),
    path('<int:course_id>/old_feedback/<int:feedback_id>/download', views.old_feedback_download, name="old_feedback_results_download"),
    path('<int:course_id>/quiz/<int:quiz_id>/download', views.quiz_download, name="quiz_results_download"),
    path('<int:course_id>/old_quiz/<int:quiz_id>/download', views.old_quiz_download, name="old_quiz_results_download")

]
