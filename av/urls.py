# oppia/av/urls.py
from django.conf.urls import url
from django.urls import path

from av import views as oppia_av_views

app_name = 'av'

urlpatterns = [
   path(r'', oppia_av_views.AVHome.as_view(), name="index"),
   path(r'view/<int:id>/',
       oppia_av_views.media_view,
       name="view"),
   path(r'view/set-image-default/<int:image_id>',
       oppia_av_views.set_default_image_view,
       name="set_default_image"),

   path(r'upload', oppia_av_views.Upload.as_view(), name="upload"),
   path(r'upload/success/<int:id>/',
       oppia_av_views.UploadSuccess.as_view(),
       name="upload_success"),
]
