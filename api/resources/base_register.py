from django.conf import settings
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from oppia.models import Points, Award
from profile.models import UserProfile, CustomField, UserProfileCustomField

from settings import constants
from settings.models import SettingProperties


class RegisterBaseResource(ModelResource):
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

    def process_register_base_profile(self, bundle):
        user_profile = UserProfile()
        user_profile.user = bundle.obj
        if 'jobtitle' in bundle.data:
            user_profile.job_title = bundle.data['jobtitle']
        if 'organisation' in bundle.data:
            user_profile.organisation = bundle.data['organisation']
        if 'phoneno' in bundle.data:
            user_profile.phone_number = bundle.data['phoneno']
        user_profile.save()

    def process_register_custom_fields(self, bundle):
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

    def dehydrate_points(self, bundle):
        points = Points.get_userscore(User.objects.get(
            username__exact=bundle.data['username']))
        return points

    def dehydrate_badges(self, bundle):
        badges = Award.get_userawards(User.objects.get(
            username__exact=bundle.data['username']))
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
