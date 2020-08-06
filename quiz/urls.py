from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views import static
from django.views.generic import TemplateView
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
