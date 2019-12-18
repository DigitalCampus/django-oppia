from django.conf.urls import url, include
from tastypie.api import Api

from activitylog.views import post_activitylog
from api.media import upload_view
from api.publish import publish_view

from api.resources.awards import AwardsResource
from api.resources.badges import BadgesResource
from api.resources.course import CourseResource
from api.resources.login import UserResource
from api.resources.points import PointsResource
from api.resources.profile_update import ProfileUpdateResource
from api.resources.register import RegisterResource
from api.resources.reset_password import ResetPasswordResource
from api.resources.tag import TagResource
from api.resources.tracker import TrackerResource

from quiz.api.resources import QuizResource, \
                               QuizPropsResource, \
                               QuestionResource, \
                               QuizQuestionResource, \
                               ResponseResource, \
                               QuizAttemptResource


def get_api(version_name):
    api = Api(api_name=version_name)
    api.register(TrackerResource())
    api.register(CourseResource())
    api.register(TagResource())
    api.register(PointsResource())
    api.register(AwardsResource())
    api.register(BadgesResource())
    api.register(UserResource())
    api.register(RegisterResource())
    api.register(ResetPasswordResource())
    api.register(ProfileUpdateResource())

    api.register(QuizResource())
    api.register(QuizPropsResource())
    api.register(QuestionResource())
    api.register(QuizQuestionResource())
    api.register(ResponseResource())
    api.register(QuizAttemptResource())

    return api


urlpatterns = [
    url(r'^', include(get_api('v1').urls)),
    url(r'^publish/$', publish_view, name="oppia_publish"),
    url(r'^media/$', upload_view, name="oppia_upload_media_api"),
    url(r'^activitylog/$', post_activitylog, name="oppia_upload_activitylog"),
]
