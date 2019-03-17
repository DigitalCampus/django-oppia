from django.conf import settings
from django.conf.urls import url, include
from tastypie.api import Api

from activitylog.views import post_activitylog
from api.media import upload_view
from api.publish import publish_view
from api.resources import TrackerResource, CourseResource, TagResource, PointsResource, AwardsResource, BadgesResource, \
    UserResource, RegisterResource, ResetPasswordResource

from quiz.api.resources import QuizResource, QuizPropsResource, QuestionResource, QuizQuestionResource, \
    ResponseResource, QuizAttemptResource


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

    api.register(QuizResource())
    api.register(QuizPropsResource())
    api.register(QuestionResource())
    api.register(QuizQuestionResource())
    api.register(ResponseResource())
    api.register(QuizAttemptResource())


    if settings.DEVICE_ADMIN_ENABLED:
        from deviceadmin.api.resources import UserDeviceResource
        api.register(UserDeviceResource())

    return api


urlpatterns = [
    url(r'^', include(get_api('v1').urls)),
    url(r'^publish/$', publish_view, name="oppia_publish"),
    url(r'^media/$', upload_view, name="oppia_upload_media_api"),
    url(r'^activitylog/$', post_activitylog, name="oppia_upload_activitylog"),
]