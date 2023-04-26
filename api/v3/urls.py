from django.urls import path, include
from rest_framework import routers

from api.v3.awards import AwardViewSet

router = routers.DefaultRouter()
router.register(r'awards', AwardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]