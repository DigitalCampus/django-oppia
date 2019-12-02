import api

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from oppia.models import Tracker, Points, Award
from profile.forms import RegisterForm
from profile.models import UserProfile, CustomField, UserProfileCustomField

from settings import constants
from settings.models import SettingProperties

from api.utils import check_required_params


class RegisterResource(ModelResource):
    '''
    For user registration
    '''
    points = fields.IntegerField(readonly=True)
    badges = fields.IntegerField(readonly=True)
    scoring = fields.BooleanField(readonly=True)
    badging = fields.BooleanField(readonly=True)
    metadata = fields.CharField(readonly=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'register'
        allowed_methods = ['post']
        fields = ['username', 'first_name', 'last_name', 'email', 'points']
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):
        self_register = SettingProperties \
            .get_int(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                     settings.OPPIA_ALLOW_SELF_REGISTRATION)
        if not self_register:
            raise BadRequest(_(u'Registration is disabled on this server.'))
        required = ['username',
                    'password',
                    'passwordagain',
                    'email',
                    'firstname',
                    'lastname']
        check_required_params(bundle, required)

        data = {'username': bundle.data['username'],
                'password': bundle.data['password'],
                'password_again': bundle.data['passwordagain'],
                'email': bundle.data['email']
                if 'email' in bundle.data else '',
                'first_name': bundle.data['firstname'],
                'last_name': bundle.data['lastname'], }

        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            try:
                data[custom_field.id] = bundle.data[custom_field.id]
            except KeyError:
                pass

        rf = RegisterForm(data)
        if not rf.is_valid():
            str = ""
            for key, value in rf.errors.items():
                for error in value:
                    str += error + "\n"
            raise BadRequest(str)
        else:
            username = bundle.data['username']
            password = bundle.data['password']
            email = bundle.data['email']
            first_name = bundle.data['firstname']
            last_name = bundle.data['lastname']

        try:
            bundle.obj = User.objects.create_user(username, email, password)
            bundle.obj.first_name = first_name
            bundle.obj.last_name = last_name
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest(
                _(u'Username "%s" already in use, please select another'
                  % username))

        user_profile = UserProfile()
        user_profile.user = bundle.obj
        if 'jobtitle' in bundle.data:
            user_profile.job_title = bundle.data['jobtitle']
        if 'organisation' in bundle.data:
            user_profile.organisation = bundle.data['organisation']
        if 'phoneno' in bundle.data:
            user_profile.phone_number = bundle.data['phoneno']
        user_profile.save()

        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            try:
                value = bundle.data[custom_field.id]
            except KeyError:
                continue

            if custom_field.type == 'int':
                profile_field = UserProfileCustomField(
                    key_name=custom_field,
                    user=bundle.obj,
                    value_int=value)
            elif custom_field.type == 'bool':
                profile_field = UserProfileCustomField(
                    key_name=custom_field,
                    user=bundle.obj,
                    value_bool=value)
            else:
                profile_field = UserProfileCustomField(
                    key_name=custom_field,
                    user=bundle.obj,
                    value_str=value)
            if (value is not None
                    and value != '') \
                    or custom_field.required is True:
                profile_field.save()

        u = authenticate(username=username, password=password)
        if u is not None and u.is_active:
            login(bundle.request, u)
            # Add to tracker
            tracker = Tracker()
            tracker.user = u
            tracker.type = 'register'
            tracker.ip = bundle.request.META.get('REMOTE_ADDR',
                                                 api.DEFAULT_IP_ADDRESS)
            tracker.agent = bundle.request.META.get('HTTP_USER_AGENT',
                                                    'unknown')
            tracker.save()
        key = ApiKey.objects.get(user=u)
        bundle.data['api_key'] = key.key

        del bundle.data['passwordagain']
        del bundle.data['password']
        del bundle.data['firstname']
        del bundle.data['lastname']
        return bundle

    def dehydrate_points(self, bundle):
        points = Points.get_userscore(User.objects.get(
            username__exact=bundle.data['username']))
        return points

    def dehydrate_badges(self, bundle):
        badges = Award.get_userawards(User.objects.get(
            username__exact=bundle.data['username']))
        return badges

    def dehydrate_scoring(self, bundle):
        return settings.OPPIA_POINTS_ENABLED

    def dehydrate_badging(self, bundle):
        return settings.OPPIA_BADGES_ENABLED

    def dehydrate_metadata(self, bundle):
        return settings.OPPIA_METADATA
