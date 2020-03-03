from django.urls import path

from content import views as content_views

app_name = 'content'
urlpatterns = [
    path('video-embed-helper/',
         content_views.media_embed_helper,
         name="video_embed_helper"),
    path('media-embed-helper/',
         content_views.media_embed_helper,
         name="media_embed_helper"),
]
