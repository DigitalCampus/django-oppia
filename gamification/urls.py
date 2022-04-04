from django.urls import path

from gamification import views as oppia_gamification_views

urlpatterns = [
    path('leaderboard/export/server',
         oppia_gamification_views.leaderboard_export,
         name="oppia_gamification_leaderboard_export_server"),
    path('leaderboard/export/<int:course_id>/',
         oppia_gamification_views.leaderboard_export,
         name="oppia_gamification_leaderboard_export_course"),
    path('points/course/<int:course_id>/',
         oppia_gamification_views.edit_course_gamification,
         name="oppia_gamification_edit_course"),

]
