from django.conf.urls import url, include
from tastypie.api import Api

from activitylog.views import post_activitylog
from api.media import upload_view
from api.publish import publish_view

from api.resources.awards import AwardsResource
from api.resources.badges import BadgesResource
from api.resources.course import CourseResource
from api.resources.login import UserResource as UserResource
from api.resources.media import MediaResource
from api.resources.points import PointsResource
from api.resources.profile_update import ProfileUpdateResource
from api.resources.v1.register import RegisterResource as RegisterResourceV1
from api.resources.v2.register import RegisterResource as RegisterResourceV2
from api.resources.reset_password import ResetPasswordResource
from api.resources.tag import TagResource
from api.resources.tracker import TrackerResource
from quiz.api.resources import QuizAttemptResource


def get_api_v1():
    api = Api(api_name='v1')
    api.register(TrackerResource())
    api.register(CourseResource())
    api.register(TagResource())
    api.register(PointsResource())
    api.register(AwardsResource())
    api.register(BadgesResource())
    api.register(UserResource())
    api.register(RegisterResourceV1())
    api.register(ResetPasswordResource())
    api.register(ProfileUpdateResource())
    api.register(QuizAttemptResource())
    return api


def get_api_v2():
    api = Api(api_name='v2')
    api.register(TrackerResource())
    api.register(CourseResource())
    api.register(TagResource())
    api.register(PointsResource())
    api.register(AwardsResource())
    api.register(BadgesResource())
    api.register(UserResource())
    api.register(RegisterResourceV2())
    api.register(ResetPasswordResource())
    api.register(ProfileUpdateResource())
    api.register(QuizAttemptResource())
    api.register(MediaResource())
    return api


urlpatterns = [
    url(r'^', include(get_api_v1().urls)),
    url(r'^', include(get_api_v2().urls)),
    url(r'^publish/$', publish_view, name="oppia_publish"),
    url(r'^media/$', upload_view, name="oppia_upload_media_api"),
    url(r'^activitylog/$', post_activitylog, name="oppia_upload_activitylog"),
]
