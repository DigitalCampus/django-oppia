from django.conf.urls import include
from django.urls import path
from tastypie.api import Api

from activitylog.views import post_activitylog
from api.media import upload_view, get_view
from api.publish import publish_view

from api.resources.awards import AwardsResource
from api.resources.badges import BadgesResource
from api.resources.course import CourseResource, CourseStructureResource
from api.resources.login import UserResource as UserResource
from api.resources.points import PointsResource
from api.resources.profile import ProfileUpdateResource, ChangePasswordResource, UserCohortsResource
from api.resources.v1.register import RegisterResource as RegisterResourceV1
from api.resources.v2.register import RegisterResource as RegisterResourceV2
from api.resources.reset_password import ResetPasswordResource
from api.resources.category import CategoryResource
from api.resources.tracker import TrackerResource
from api.resources.username import UsernameResource
from api.resources.progress import UserCourseSummaryResource
from api.resources.delete_account import DeleteAccountResource
from api.resources.download_data import DownloadDataResource
from quiz.api.resources import QuizAttemptResource


def get_api_v1():
    api = Api(api_name='v1')
    api.register(TrackerResource())
    api.register(CourseResource())
    api.register(CategoryResource())
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
    api.register(CategoryResource())
    api.register(PointsResource())
    api.register(AwardsResource())
    api.register(BadgesResource())
    api.register(UserResource())
    api.register(RegisterResourceV2())
    api.register(ResetPasswordResource())
    api.register(ProfileUpdateResource())
    api.register(QuizAttemptResource())
    api.register(CourseStructureResource())
    api.register(UserCourseSummaryResource())
    api.register(UsernameResource())
    api.register(DeleteAccountResource())
    api.register(DownloadDataResource())
    api.register(ChangePasswordResource())
    api.register(UserCohortsResource())
    return api


urlpatterns = [
    path('', include(get_api_v1().urls)),
    path('', include(get_api_v2().urls)),
    path('publish/', publish_view, name="oppia_publish"),
    path('media/', upload_view, name="oppia_upload_media_api"),
    path('activitylog/', post_activitylog, name="oppia_upload_activitylog"),
    path('media/<str:digest>', get_view, name="get_upload_media_api"),
]
