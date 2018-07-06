# oppia/urls.py
from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views import static

from oppia.api.resources import TrackerResource, CourseResource, TagResource
from oppia.api.resources import PointsResource, AwardsResource, BadgesResource, RegisterResource, UserResource, ResetPasswordResource

from oppia.quiz.api.resources import QuizResource, QuizPropsResource, QuestionResource
from oppia.quiz.api.resources import QuizQuestionResource, ResponseResource, QuizAttemptResource

from oppia import views as oppia_views
from oppia.api import publish as oppia_api_publish
from oppia.api import media as oppia_api_media

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(TrackerResource())
v1_api.register(CourseResource())
v1_api.register(TagResource())
v1_api.register(PointsResource())
v1_api.register(AwardsResource())
v1_api.register(BadgesResource())
v1_api.register(UserResource())
v1_api.register(RegisterResource())
v1_api.register(ResetPasswordResource())

v1_api.register(QuizResource())
v1_api.register(QuizPropsResource())
v1_api.register(QuestionResource())
v1_api.register(QuizQuestionResource())
v1_api.register(ResponseResource())
v1_api.register(QuizAttemptResource())

if settings.DEVICE_ADMIN_ENABLED:
    from oppia.deviceadmin.api.resources import UserDeviceResource

    v1_api.register(UserDeviceResource())

#Custom HTTP response pages
handler403 = 'oppia.permissions.oppia_403_handler'

urlpatterns = [

    url(r'^$', oppia_views.home_view, name="oppia_home"),
    url(r'^server/$', oppia_views.server_view, name="oppia_server"),
    url(r'^about/$', oppia_views.about_view, name="oppia_about"),
    
    url(r'^teacher/$', oppia_views.teacher_home_view, name="oppia_teacher_home"),
    
    url(r'^leaderboard/$', oppia_views.leaderboard_view, name="oppia_leaderboard"),
    url(r'^upload/$', oppia_views.upload_step1, name="oppia_upload"),
    url(r'^upload2/(?P<course_id>\d+)$', oppia_views.upload_step2, name="oppia_upload2"),
    url(r'^upload2/success/$', TemplateView.as_view(template_name="oppia/upload-success.html"), name="oppia_upload_success"),
    url(r'^course/$', oppia_views.courses_list_view, name="oppia_course"),
    url(r'^course/tag/(?P<tag_id>\d+)/$', oppia_views.tag_courses_view, name="oppia_tag_courses"),
    url(r'^course/(?P<course_id>\d+)/$', oppia_views.recent_activity, name="oppia_recent_activity"),
    url(r'^course/(?P<course_id>\d+)/edit/$', oppia_views.upload_step2, {'editing': True}, name="oppia_course_edit"),
    url(r'^course/(?P<course_id>\d+)/detail/$', oppia_views.recent_activity_detail, name="oppia_recent_activity_detail"),
    url(r'^course/(?P<course_id>\d+)/detail/export/$', oppia_views.export_tracker_detail, name="oppia_export_tracker_detail"),
    url(r'^course/(?P<course_id>\d+)/download/$', oppia_views.course_download_view, name="oppia_course_download"),
    url(r'^course/(?P<course_id>\d+)/quiz/$', oppia_views.course_quiz, name="oppia_course_quiz"),
    url(r'^course/(?P<course_id>\d+)/quiz/(?P<quiz_id>\d+)/attempts/$', oppia_views.course_quiz_attempts, name="oppia_course_quiz_attempts"),
    url(r'^course/(?P<course_id>\d+)/feedback/$', oppia_views.course_feedback, name="oppia_course_feedback"),
    url(r'^course/(?P<course_id>\d+)/feedback/(?P<quiz_id>\d+)/responses/$', oppia_views.course_feedback_responses, name="oppia_course_feedback_responses"),
    
    url(r'^cohort/$', oppia_views.cohort_list_view, name="oppia_cohorts"),
    url(r'^cohort/add/$', oppia_views.cohort_add, name="oppia_cohort_add"),
    url(r'^cohort/(?P<cohort_id>\d+)/edit/$', oppia_views.cohort_edit, name="oppia_cohort_edit"),
    url(r'^cohort/(?P<cohort_id>\d+)/view/$', oppia_views.cohort_view, name="oppia_cohort_view"),
    url(r'^cohort/(?P<cohort_id>\d+)/(?P<course_id>\d+)/view/$', oppia_views.cohort_course_view, name="oppia_cohort_course_view"),
    url(r'^cohort/(?P<cohort_id>\d+)/leaderboard/$', oppia_views.cohort_leaderboard_view, name="oppia_cohort_leaderboard"),
    
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/publish/$', oppia_api_publish.publish_view, name="oppia_publish"),
    url(r'^api/media/$', oppia_api_media.upload_view, name="oppia_upload_media_api"),
    
    url(r'^content/', include('oppia.content.urls')),
    url(r'^preview/', include('oppia.preview.urls')),
    url(r'^profile/', include('oppia.profile.urls')),
    url(r'^mobile/', include('oppia.mobile.urls')),
    url(r'^reports/', include('oppia.reports.urls')),
    url(r'^activitylog/', include('oppia.activitylog.urls')),
    url(r'^viz/', include('oppia.viz.urls')),
    url(r'^av/', include('oppia.av.urls')),
    url(r'^gamification/', include('oppia.gamification.urls')),
    
    url(r'^view/$', oppia_views.app_launch_activity_redirect_view, name="oppia_app_launch_activity_redirect"),
    
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEVICE_ADMIN_ENABLED:
    gcmpatterns = [
        url(r'^deviceadmin/', include('oppia.deviceadmin.urls')),
    ]
    urlpatterns += gcmpatterns
