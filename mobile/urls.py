# oppia/mobile/urls.py
from django.conf.urls import url

from mobile import views as oppia_mobile_views

urlpatterns = [
    url(r'^scorecard/$', oppia_mobile_views.scorecard_view, name="oppia_mobile_scorecard"),
]
