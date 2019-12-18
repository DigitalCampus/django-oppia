import api

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from api.serializers import UserJSONSerializer
from oppia.models import Tracker
from oppia.models import Points, Award


class UserResource(ModelResource):
    '''
    For user login

    Usage:
    POST request to ``http://localhost/api/v1/user/``

    Required arguments:

    * ``username``
    * ``password``

    Returns (if authorized):

    Object with ``first_name``,
                ``last_name``,
                ``api_key``,
                ``last_login``,
                ``username``,
                ``points``,
                ``badges``,
                and ``scoring``

    If unauthorized returns an HTTP 401 response

    '''
    points = fields.IntegerField(readonly=True)
    badges = fields.IntegerField(readonly=True)
    scoring = fields.BooleanField(readonly=True)
    badging = fields.BooleanField(readonly=True)
    metadata = fields.CharField(readonly=True)
    course_points = fields.CharField(readonly=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['first_name',
                  'last_name',
                  'last_login',
                  'username',
                  'points',
                  'badges']
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
        if u is not None:
            if u.is_active:
                login(bundle.request, u)
                # Add to tracker
                tracker = Tracker()
                tracker.user = u
                tracker.type = 'login'
                tracker.ip = bundle.request.META.get('REMOTE_ADDR',
                                                     api.DEFAULT_IP_ADDRESS)
                tracker.agent = bundle.request.META.get('HTTP_USER_AGENT',
                                                        'unknown')
                tracker.save()
            else:
                raise BadRequest(_(u'Authentication failure'))
        else:
            raise BadRequest(_(u'Authentication failure'))

        del bundle.data['password']
        key = ApiKey.objects.get(user=u)
        bundle.data['api_key'] = key.key
        bundle.obj = u
        return bundle

    def dehydrate_points(self, bundle):
        points = Points.get_userscore(
            User.objects.get(username=bundle.request.user.username))
        return points

    def dehydrate_badges(self, bundle):
        badges = Award.get_userawards(
            User.objects.get(username=bundle.request.user.username))
        return badges

    def dehydrate_scoring(self, bundle):
        return settings.OPPIA_POINTS_ENABLED

    def dehydrate_badging(self, bundle):
        return settings.OPPIA_BADGES_ENABLED

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
