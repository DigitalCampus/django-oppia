# av/urls.py
from django.urls import path

from av import views

app_name = 'av'

urlpatterns = [
    path('', views.AVHome.as_view(), name="index"),
    path('view/<int:id>', views.media_view, name="view"),
    path('view/set-image-default/<int:image_id>',
         views.set_default_image_view,
         name="set_default_image"),
    path('upload', views.Upload.as_view(), name="upload"),
    path('upload/success/<int:id>/',
         views.UploadSuccess.as_view(),
         name="upload_success"),
    path('course/<int:course_id>/media/',
         views.CourseMediaList.as_view(),
         name="course_media"),
    path('course/<int:course_id>/download/',
         views.download_course_media,
         name="download_course_media"),
]
