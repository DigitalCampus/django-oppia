# av/urls.py
from django.urls import path

from av import views as av_views

app_name = 'av'

urlpatterns = [
   path('', av_views.AVHome.as_view(), name="index"),
   path('view/<int:id>/', av_views.media_view, name="view"),
   path('view/set-image-default/<int:image_id>',
        av_views.set_default_image_view,
        name="set_default_image"),
   path('upload', av_views.Upload.as_view(), name="upload"),
   path('upload/success/<int:id>/',
        av_views.UploadSuccess.as_view(),
        name="upload_success"),
]
