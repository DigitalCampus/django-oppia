
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from api.serializers import UserJSONSerializer
from oppia import DEFAULT_IP_ADDRESS
from oppia.models import Tracker, Participant
from oppia.models import Points, Award

from profile.models import UserProfile

from settings import constants
from settings.models import SettingProperties


class UserResource(ModelResource):

    points = fields.IntegerField(readonly=True)
    badges = fields.IntegerField(readonly=True)
    scoring = fields.BooleanField(readonly=True)
    badging = fields.BooleanField(readonly=True)
    metadata = fields.CharField(readonly=True)
    course_points = fields.CharField(readonly=True)
    cohorts = fields.CharField(readonly=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['first_name',
                  'last_name',
                  'last_login',
                  'username',
                  'points',
                  'badges',
                  'email',
                  'job_title',
                  'organisation']

        allowed_methods = ['post']
        authentication = Authentication()
        authorization = Authorization()
        serializer = UserJSONSerializer()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):

        if 'username' not in bundle.data:
            raise BadRequest(_(u'Username missing'))

        if 'password' not in bundle.data:
            raise BadRequest(_(u'Password missing'))

        username = bundle.data['username']
        password = bundle.data['password']

        u = authenticate(username=username, password=password)
        if u is not None and u.is_active:
            login(bundle.request, u)
            # Add to tracker
            tracker = Tracker()
            tracker.user = u
            tracker.type = 'login'
            tracker.ip = bundle.request.META.get('REMOTE_ADDR',
                                                 DEFAULT_IP_ADDRESS)
            tracker.agent = bundle.request.META.get('HTTP_USER_AGENT',
                                                    'unknown')
            tracker.save()
        else:
            raise BadRequest(_(u'Authentication failure'))

        del bundle.data['password']
        key = ApiKey.objects.get(user=u)
        bundle.data['api_key'] = key.key

        try:
            up = UserProfile.objects.get(user__username=username)
            job_title = up.job_title
            organisation = up.organisation
        except UserProfile.DoesNotExist:
            job_title = ""
            organisation = ""

        bundle.data['job_title'] = job_title
        bundle.data['organisation'] = organisation
        bundle.obj = u
        return bundle

    def dehydrate_cohorts(self, bundle):
        return Participant.get_user_cohorts(bundle.request.user)

    def dehydrate_points(self, bundle):
        points = Points.get_userscore(
            User.objects.get(username=bundle.request.user.username))
        return points

    def dehydrate_badges(self, bundle):
        badges = Award.get_userawards(
            User.objects.get(username=bundle.request.user.username))
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
            Points.objects
            .exclude(course=None)
            .filter(user=bundle.request.user)
            .values('course__shortname')
            .annotate(total_points=Sum('points')))
        return course_points
