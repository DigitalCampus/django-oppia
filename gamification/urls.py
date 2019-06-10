from django.conf.urls import url

from gamification import views as oppia_gamification_views

urlpatterns = [
    url(r'^leaderboard/export/server$', oppia_gamification_views.leaderboard_export, name="oppia_gamification_leaderboard_export_server"),
    url(r'^leaderboard/export/(?P<course_id>\d+)/$', oppia_gamification_views.leaderboard_export, name="oppia_gamification_leaderboard_export_course"),
    url(r'^points/course/(?P<course_id>\d+)/edit/$', oppia_gamification_views.edit_course_points, name="oppia_gamification_edit_course_points"),
    url(r'^points/course/(?P<course_id>\d+)/updated/$', oppia_gamification_views.course_points_updated, name="oppia_gamification_course_points_updated"),
    
    url(r'^points/activity/(?P<course_id>\d+)/view/$', oppia_gamification_views.view_activity_points, name="oppia_gamification_view_activity_points"),
    url(r'^points/activity/(?P<course_id>\d+)/edit/(?P<activity_id>\d+)/$', oppia_gamification_views.edit_activity_points, name="oppia_gamification_edit_activity_points"),
    
    url(r'^points/media/(?P<course_id>\d+)/view/$', oppia_gamification_views.view_media_points, name="oppia_gamification_view_media_points"),
    url(r'^points/media/(?P<course_id>\d+)/edit/(?P<media_id>\d+)/$', oppia_gamification_views.edit_media_points, name="oppia_gamification_edit_media_points"),
]
