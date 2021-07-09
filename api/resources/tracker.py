import json
import datetime

from django.conf import settings

from django.db.models import Sum
from django.http import HttpResponse
from django.utils import dateparse

from json.decoder import JSONDecodeError
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, \
                               convert_post_to_patch, \
                               dict_strip_unicode_keys
from tastypie.utils import timezone

from api.serializers import PrettyJSONSerializer
from oppia import DEFAULT_IP_ADDRESS
from oppia.models import Activity, Tracker, Media, Points, Award

from api.resources.login import UserResource
from api.validation import TrackerValidation

from settings import constants
from settings.models import SettingProperties


class TrackerResource(ModelResource):
    '''
    Submitting a Tracker
    '''
    user = fields.ForeignKey(UserResource, 'user')
    points = fields.IntegerField(readonly=True)
    badges = fields.IntegerField(readonly=True)
    scoring = fields.BooleanField(readonly=True)
    badging = fields.BooleanField(readonly=True)
    metadata = fields.CharField(readonly=True)
    course_points = fields.CharField(readonly=True)

    class Meta:
        queryset = Tracker.objects.all()
        resource_name = 'tracker'
        allowed_methods = ['post', 'patch']
        detail_allowed_methods = ['post', 'patch']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = PrettyJSONSerializer()
        always_return_data = True
        fields = ['points',
                  'digest',
                  'data',
                  'tracker_date',
                  'badges',
                  'course',
                  'completed',
                  'scoring',
                  'metadata',
                  'badging']
        validation = TrackerValidation()

    def process_tracker_bundle(self, bundle):
        try:
            if 'course' in bundle.data and 'digest' in bundle.data:
                media = Media.objects.filter(
                    digest=bundle.data['digest'],
                    course__shortname=bundle.data['course']).first()
            elif 'digest' in bundle.data:
                media = Media.objects.filter(
                    digest=bundle.data['digest']).first()
            else:
                media = None

            if media is not None:
                bundle.obj.course = media.course
                bundle.obj.type = 'media'
        except Media.DoesNotExist:
            pass

        try:
            json_data = json.loads(bundle.data['data'])
            if 'timetaken' in json_data:
                bundle.obj.time_taken = json_data['timetaken']
            if 'uuid' in json_data:
                bundle.obj.uuid = json_data['uuid']
            if 'lang' in json_data:
                bundle.obj.lang = json_data['lang']
        except ValueError:
            pass
        except KeyError:
            pass
        except TypeError:  # means json_data is None
            pass

        if 'points' in bundle.data:
            bundle.obj.points = bundle.data['points']

        if 'event' in bundle.data:
            bundle.obj.event = bundle.data['event']

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()
    
        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        self.authorized_create_detail(self.get_object_list(bundle.request),
                                      bundle)
        bundle = self.full_hydrate(bundle)

        if bundle.obj.type == 'search':
            if not bundle.obj.data:
                return bundle
            try:
                json_data = json.loads(bundle.obj.data)
                if 'query' not in json_data \
                        or json_data['query'] is None \
                        or json_data['query'].strip() == "":
                    return bundle
            except JSONDecodeError:
                return bundle
        return self.save(bundle)

    def hydrate(self, bundle, request=None):

        # remove any id if this is submitted - otherwise it may overwrite
        # existing tracker item
        if 'id' in bundle.data:
            del bundle.obj.id
        bundle.obj.user = bundle.request.user
        bundle.obj.ip = bundle.request.META.get('REMOTE_ADDR',
                                                DEFAULT_IP_ADDRESS)
        bundle.obj.agent = bundle.request.META.get('HTTP_USER_AGENT',
                                                   'unknown')

        if 'type' in bundle.data and bundle.data['type'] == 'search':
            # if the tracker is a search, we just need to save it
            bundle.obj.course = None
            bundle.obj.type = "search"
            return bundle

        # find out the course & activity type from the digest
        if 'course' in bundle.data:
            activity = Activity.objects \
                .filter(
                    digest=bundle.data['digest'],
                    section__course__shortname=bundle.data['course']) \
                .first()
        elif 'digest' in bundle.data:
            activity = Activity.objects.filter(
                digest=bundle.data['digest']).first()
        else:
            activity = None

        if activity is not None:
            bundle.obj.course = activity.section.course
            bundle.obj.type = activity.type
            bundle.obj.activity_title = activity.title
            bundle.obj.section_title = activity.section.title
        else:
            bundle.obj.course = None
            bundle.obj.type = ''
            bundle.obj.activity_title = ''
            bundle.obj.section_title = ''

        bundle = self.process_tracker_bundle(bundle)

        return bundle

    def hydrate_tracker_date(self, bundle, request=None, **kwargs):
        # Fix tracker date if date submitted is in the future
        if 'tracker_date' in bundle.data:
            tracker_date = dateparse.parse_datetime(
                bundle.data['tracker_date'])
            if tracker_date > datetime.datetime.now():
                bundle.data['tracker_date'] = timezone.now()

        return bundle

    def dehydrate_points(self, bundle):
        points = Points.get_userscore(bundle.request.user)
        return points

    def dehydrate_badges(self, bundle):
        badges = Award.get_userawards(bundle.request.user)
        return badges

    def dehydrate_scoring(self, bundle):
        return SettingProperties.get_bool(
            constants.OPPIA_POINTS_ENABLED,
            settings.OPPIA_POINTS_ENABLED)

    def dehydrate_badging(self, bundle):
        return SettingProperties.get_bool(
            constants.OPPIA_BADGES_ENABLED,
            settings.OPPIA_BADGES_ENABLED)

    def dehydrate_metadata(self, bundle):
        return settings.OPPIA_METADATA

    def dehydrate_course_points(self, bundle):
        course_points = list(
            Points.objects.exclude(course=None)
            .filter(user=bundle.request.user)
            .values('course__shortname')
            .annotate(total_points=Sum('points')))
        return course_points

    def patch_list(self, request, **kwargs):
        request = convert_post_to_patch(request)
        deserialized = self.deserialize(
            request,
            request.body,
            format=request.META.get('CONTENT_TYPE',
                                    'application/json'))
        for data in deserialized.get("objects"):
            data = self.alter_deserialized_detail_data(request, data)
            bundle = self.build_bundle(data=dict_strip_unicode_keys(data))
            bundle.request.user = request.user
            bundle.request.META['REMOTE_ADDR'] = \
                request.META.get('REMOTE_ADDR', DEFAULT_IP_ADDRESS)
            bundle.request.META['HTTP_USER_AGENT'] = \
                request.META.get('HTTP_USER_AGENT', 'unknown')
            # check UUID not already submitted
            if 'data' in bundle.data:
                json_data = json.loads(bundle.data['data'])
                if 'uuid' in json_data:
                    uuids = Tracker.objects.filter(uuid=json_data['uuid'])
                    if uuids.count() == 0:
                        self.obj_create(bundle, request=request)
                else:
                    self.obj_create(bundle, request=request)
            else:
                self.obj_create(bundle, request=request)

        response_data = {'points': self.dehydrate_points(bundle),
                         'badges': self.dehydrate_badges(bundle),
                         'scoring': self.dehydrate_scoring(bundle),
                         'badging': self.dehydrate_badging(bundle),
                         'metadata': self.dehydrate_metadata(bundle),
                         'course_points': self.dehydrate_course_points(bundle),
                         }
        response = HttpResponse(content=json.dumps(response_data),
                                content_type="application/json; charset=utf-8")
        return response
