# av/urls.py
from django.urls import path

from av import views

app_name = 'av'

urlpatterns = [
    path('', views.AVHome.as_view(), name="index"),
    path('course/<int:course_id>/media/',
         views.CourseMediaList.as_view(),
         name="course_media"),
    path('media/<int:media_id>/download/',
         views.download_media_file,
         name="download_media_file"),

    path('course/<int:course_id>/download/',
         views.download_course_media,
         name="download_course_media"),
]
