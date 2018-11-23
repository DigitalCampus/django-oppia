# oppia/content/urls.py
from django.conf.urls import url

from content import views as oppia_content_views

urlpatterns = [
                url(r'^video-embed-helper/$', oppia_content_views.media_embed_helper, name="oppia_video_embed_helper"),
                url(r'^media-embed-helper/$', oppia_content_views.media_embed_helper, name="oppia_media_embed_helper"),
        ]
