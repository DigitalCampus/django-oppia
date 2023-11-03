import warnings

from django.urls import path, include
from tastypie.api import Api

from activitylog.views import post_activitylog

from api.v3 import urls as apiv3urls
from api.media import upload_view, get_view
from api.publish import publish_view

from api.resources.awards import AwardsResource
from api.resources.badges import BadgesResource
from api.resources.course import CourseResource, CourseStructureResource
from api.resources.login import UserResource as UserResource
from api.resources.points import PointsResource
from api.resources.profile import ProfileUpdateResource, ChangePasswordResource, UserCohortsResource, \
    UserProfileResource
from api.resources.v2.register import RegisterResource as RegisterResourceV2
from api.resources.reset_password import ResetPasswordResource
from api.resources.category import CategoryResource
from api.resources.tracker import TrackerResource
from api.resources.username import UsernameResource
from api.resources.progress import UserCourseSummaryResource
from api.resources.delete_account import DeleteAccountResource
from api.resources.download_data import DownloadDataResource
from quiz.api.resources import QuizAttemptResource


# warnings.warn("API v2 will be removed in v0.16.0", DeprecationWarning, stacklevel=2)


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
    api.register(UserProfileResource())
    return api


urlpatterns = [
    # for API v2
    path('', include(get_api_v2().urls)),
    path('publish/', publish_view, name="oppia_publish"),
    path('media/', upload_view, name="oppia_upload_media_api"),
    path('activitylog/', post_activitylog, name="oppia_upload_activitylog"),
    path('media/<str:digest>', get_view, name="get_upload_media_api"),

    # for API v3
    path('v3/', include(apiv3urls)),
]
