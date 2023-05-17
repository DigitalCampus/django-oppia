from django.urls import path, include
from rest_framework import routers

from api.v3.award import AwardViewSet
from api.v3.badge import BadgeViewSet
from api.v3.user import UserViewSet
from api.v3.category import CategoryViewSet
from api.v3.course import CourseViewSet
from api.v3.userdata import UserDataViewSet
from api.v3.activitylog import ActivityLogViewSet
from api.v3.login import LoginViewSet
from api.v3.media import MediaViewSet
from api.v3.points import PointsViewSet
from api.v3.leaderboard import LeaderboardViewSet

# Uncomment once ready to be deployed
router = routers.DefaultRouter()
# router.register(r'award', AwardViewSet)
# router.register(r'badge', BadgeViewSet)
# router.register(r'user', UserViewSet)
# router.register(r'category', CategoryViewSet)
# router.register(r'course', CourseViewSet)
# router.register(r'userdata', UserDataViewSet)
# router.register(r'activitylog', ActivityLogViewSet)
# router.register(r'login', LoginViewSet)
# router.register(r'media', MediaViewSet)
# router.register(r'points', MediaViewSet)
# router.register(r'leaderboard', LeaderboardViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
