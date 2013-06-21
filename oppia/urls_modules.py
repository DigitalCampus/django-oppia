# oppia.urls_modules.py
''' This is a temporary fix for any old urls being used 
TODO: remove this after everyone has moved to new mobile app '''
from django.conf.urls import patterns, include, url
from oppia.api.resources import TrackerResource, ModuleResource, ScheduleResource, TagResource, ScorecardResource
from django.views.generic import TemplateView

from tastypie.api import Api
v1_api = Api(api_name='v1')
v1_api.register(TrackerResource())
v1_api.register(ModuleResource())
v1_api.register(ScheduleResource())
v1_api.register(TagResource())
v1_api.register(ScorecardResource())

urlpatterns = patterns('',

    (r'^api/', include(v1_api.urls)),

)