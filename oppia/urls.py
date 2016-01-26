# oppia/urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from oppia.api.resources import TrackerResource, CourseResource, ScheduleResource, TagResource
from oppia.api.resources import PointsResource, AwardsResource, BadgesResource, RegisterResource, UserResource, ResetPasswordResource
from oppia.quiz.api.resources import QuizResource, QuizPropsResource, QuestionResource
from oppia.quiz.api.resources import QuizQuestionResource, ResponseResource, QuizAttemptResource

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(TrackerResource())
v1_api.register(CourseResource())
v1_api.register(ScheduleResource())
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

urlpatterns = patterns('',

    url(r'^$', 'oppia.views.home_view', name="oppia_home"),
    url(r'^server/$', 'oppia.views.server_view', name="oppia_server"),
    url(r'^about/$', 'oppia.views.about_view', name="oppia_about"),
    
    url(r'^teacher/$', 'oppia.views.teacher_home_view', name="oppia_teacher_home"),
    
    url(r'^leaderboard/$', 'oppia.views.leaderboard_view', name="oppia_leaderboard"),
    url(r'^upload/$', 'oppia.views.upload_step1', name="oppia_upload"),
    url(r'^upload2/(?P<course_id>\d+)$', 'oppia.views.upload_step2', name="oppia_upload2"),
    url(r'^upload2/success/$', TemplateView.as_view(template_name="oppia/upload-success.html"), name="oppia_upload_success"),
    url(r'^course/$', 'oppia.views.courses_list_view', name="oppia_course"),
    url(r'^course/tag/(?P<tag_id>\d+)/$', 'oppia.views.tag_courses_view', name="oppia_tag_courses"),
    url(r'^course/(?P<course_id>\d+)/$', 'oppia.views.recent_activity', name="oppia_recent_activity"),
    url(r'^course/(?P<course_id>\d+)/detail/$', 'oppia.views.recent_activity_detail', name="oppia_recent_activity_detail"),
    url(r'^course/(?P<course_id>\d+)/detail/export/$', 'oppia.views.export_tracker_detail', name="oppia_export_tracker_detail"),
    url(r'^course/(?P<course_id>\d+)/schedule/$', 'oppia.views.schedule', name="oppia_schedules"),
    url(r'^course/(?P<course_id>\d+)/download/$', 'oppia.views.course_download_view', name="oppia_course_download"),
    url(r'^course/(?P<course_id>\d+)/schedule/add/$', 'oppia.views.schedule_add', name="oppia_schedule_add"),
    url(r'^course/(?P<course_id>\d+)/schedule/(?P<schedule_id>\d+)/edit/$', 'oppia.views.schedule_edit', name="oppia_schedule_edit"),
    url(r'^course/(?P<course_id>\d+)/schedule/saved/$', 'oppia.views.schedule_saved'),
    url(r'^course/(?P<course_id>\d+)/schedule/(?P<schedule_id>\d+)/saved/$', 'oppia.views.schedule_saved'),
    url(r'^course/(?P<course_id>\d+)/quiz/$', 'oppia.views.course_quiz', name="oppia_course_quiz"),
    url(r'^course/(?P<course_id>\d+)/quiz/(?P<quiz_id>\d+)/attempts/$', 'oppia.views.course_quiz_attempts', name="oppia_course_quiz_attempts"),
    url(r'^course/(?P<course_id>\d+)/feedback/$', 'oppia.views.course_feedback', name="oppia_course_feedback"),
    url(r'^course/(?P<course_id>\d+)/feedback/(?P<quiz_id>\d+)/responses/$', 'oppia.views.course_feedback_responses', name="oppia_course_feedback_responses"),
    
    url(r'^cohort/$', 'oppia.views.cohort_list_view', name="oppia_cohorts"),
    url(r'^cohort/add/$', 'oppia.views.cohort_add', name="oppia_cohort_add"),
    url(r'^cohort/(?P<cohort_id>\d+)/edit/$', 'oppia.views.cohort_edit', name="oppia_cohort_edit"),
    url(r'^cohort/(?P<cohort_id>\d+)/view/$', 'oppia.views.cohort_view', name="oppia_cohort_view"),
    url(r'^cohort/(?P<cohort_id>\d+)/(?P<course_id>\d+)/view/$', 'oppia.views.cohort_course_view', name="oppia_cohort_course_view"),
    url(r'^cohort/(?P<cohort_id>\d+)/leaderboard/$', 'oppia.views.cohort_leaderboard_view', name="oppia_cohort_leaderboard"),
    
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/publish/$', 'oppia.api.publish.publish_view', name="oppia_publish"),
    
    url(r'^content/', include('oppia.content.urls')),
    url(r'^preview/', include('oppia.preview.urls')),
    url(r'^profile/', include('oppia.profile.urls')),
    url(r'^mobile/', include('oppia.mobile.urls')),
    url(r'^reports/', include('oppia.reports.urls')),
    url(r'^viz/', include('oppia.viz.urls')),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    
)
