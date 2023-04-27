from django.urls import path, include
from rest_framework import routers

from api.v3.award import AwardViewSet
from api.v3.badge import BadgeViewSet
from api.v3.user import UserViewSet

# Uncomment once ready to be deployed
router = routers.DefaultRouter()
# router.register(r'award', AwardViewSet)
# router.register(r'badge', BadgeViewSet)
# router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]