''' This is a temporary fix for any old urls being used 
TODO: remove this after everyone has moved to new mobile app '''
from django.conf.urls import patterns, include, url
from tastypie.api import Api
from oppia.api.resources import PointsResource, AwardsResource, BadgesResource

v1_api = Api(api_name='v1')
v1_api.register(PointsResource())
v1_api.register(AwardsResource())
v1_api.register(BadgesResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
)