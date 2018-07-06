from django.conf.urls import url

from oppia.gamification import views as oppia_gamification_views

urlpatterns = [
    url(r'^leaderboard/export/server$', oppia_gamification_views.leaderboard_export, name="oppia_gamification_leaderboard_export_server"),
    url(r'^leaderboard/export/(?P<course_id>\d+)/$', oppia_gamification_views.leaderboard_export, name="oppia_gamification_leaderboard_export_course"),
]
