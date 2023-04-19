from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, Unauthorized, ImmediateHttpResponse
from tastypie.resources import ModelResource, Resource

from api.serializers import UserJSONSerializer
from api.utils import check_required_params
from datarecovery.models import DataRecovery
from oppia.models import Participant, Points, Award
from profile.forms import ProfileForm
from profile.models import UserProfile, CustomField
from settings.models import SettingProperties
from settings import constants


class ProfileUpdateResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'profileupdate'
        allowed_methods = ['post']
        fields = ['first_name', 'last_name', 'email']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        serializer = UserJSONSerializer()
        always_return_data = True
        include_resource_uri = False

    def process_profile_update_base_profile(self, bundle):
        user_profile, created = UserProfile.objects \
            .get_or_create(user=bundle.obj)
        if 'job_title' in bundle.data:
            user_profile.job_title = bundle.data['job_title']
        if 'organisation' in bundle.data:
            user_profile.organisation = bundle.data['organisation']
        if 'phoneno' in bundle.data:
            user_profile.phone_number = bundle.data['phoneno']
        user_profile.save()
        return user_profile

    def process_profile_update(self, bundle):
        errors = []
        data = {'email': bundle.data['email']
                if 'email' in bundle.data else '',
                'first_name': bundle.data['first_name'],
                'last_name': bundle.data['last_name'],
                'username': bundle.request.user}

        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            try:
                data[custom_field.id] = bundle.data[custom_field.id]
            except KeyError:
                pass

        profile_form = ProfileForm(data=data)
        if not profile_form.is_valid():
            error_str = ""
            for key, value in profile_form.errors.items():
                for error in value:
                    error_str += error + "\n"
            raise BadRequest(error_str)
        else:
            email = bundle.data['email'] if 'email' in bundle.data else ''
            first_name = bundle.data['first_name']
            last_name = bundle.data['last_name']

        try:
            user = User.objects.get(username=bundle.request.user)
            bundle.obj = user
            bundle.obj.first_name = first_name
            bundle.obj.last_name = last_name
            bundle.obj.email = email
            bundle.obj.save()
        except User.DoesNotExist:
            raise BadRequest(_(u'Username not found'))

        # Create base UserProfile
        user_profile = self.process_profile_update_base_profile(bundle)
        # Create any CustomField entries
        user_fields = [f.name for f in User._meta.get_fields()]
        custom_fields = {field: bundle.data[field] for field in bundle.data if field not in user_fields}
        update_custom_fields_errors = user_profile.update_customfields(custom_fields)

        if update_custom_fields_errors:
            errors += update_custom_fields_errors

        if errors:
            DataRecovery.create_data_recovery_entry(
                user=user,
                data_type=DataRecovery.Type.USER_PROFILE,
                reasons=errors,
                data=bundle.data
            )

        return bundle

    def obj_create(self, bundle, **kwargs):
        required = ['first_name',
                    'last_name']
        check_required_params(bundle, required)

        # can't edit another users account
        if 'username' in bundle.data \
                and bundle.data['username'] != bundle.request.user:
            raise Unauthorized(_("You cannot edit another users profile"))

        bundle = self.process_profile_update(bundle)
        return bundle


class UserCohortsResource(Resource):

    class Meta:
        resource_name = 'cohorts'
        allowed_methods = ['get']
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        include_resource_uri = False

    def get_list(self, request, **kwargs):
        cohorts = Participant.get_user_cohorts(request.user)
        return self.create_response(request, cohorts)


class UserProfileResource(ModelResource):

    badges = fields.IntegerField(readonly=True)
    course_points = fields.CharField(readonly=True)
    cohorts = fields.CharField(readonly=True)
    scoring = fields.BooleanField(readonly=True)
    badging = fields.BooleanField(readonly=True)
    metadata = fields.CharField(readonly=True)
    points = fields.IntegerField(readonly=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'profile'
        allowed_methods = ['get']
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        include_resource_uri = False
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'job_title',
                  'organisation']

    def dispatch(self, request_type, request, **kwargs):
        # Force this to be a single User object
        return super().dispatch('detail', request, **kwargs)

    def obj_get(self, bundle, **kwargs):
        return bundle.request.user

    def dehydrate(self, bundle):
        bundle = super().dehydrate(bundle)

        try:
            profile = UserProfile.objects.get(user=bundle.obj)
            bundle.data['job_title'] = profile.job_title
            bundle.data['organisation'] = profile.organisation

            customfields = profile.get_customfields_dict()
            bundle.data.update(customfields)

        except UserProfile.DoesNotExist:
            bundle.data['job_title'] = ''
            bundle.data['organisation'] = ''

        return bundle

    def dehydrate_cohorts(self, bundle):
        return Participant.get_user_cohorts(bundle.request.user)

    def dehydrate_metadata(self, bundle):
        return settings.OPPIA_METADATA

    def dehydrate_points(self, bundle):
        return Points.get_userscore(bundle.request.user)

    def dehydrate_badges(self, bundle):
        return Award.get_userawards(bundle.request.user)

    def dehydrate_scoring(self, bundle):
        return SettingProperties.get_bool(
            constants.OPPIA_POINTS_ENABLED,
            settings.OPPIA_POINTS_ENABLED)

    def dehydrate_badging(self, bundle):
        return SettingProperties.get_bool(
            constants.OPPIA_BADGES_ENABLED,
            settings.OPPIA_BADGES_ENABLED)


class ChangePasswordResource(ModelResource):
    '''
    For resetting user password
    '''
    message = fields.CharField()

    class Meta:
        queryset = User.objects.all()
        resource_name = 'password'
        allowed_methods = ['post']
        fields = []
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        always_return_data = False
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):

        if bundle.request.user:
            form = SetPasswordForm(bundle.request.user, data=bundle.data)
            if form.is_valid():
                bundle.obj = form.save()
            else:
                raise ImmediateHttpResponse(response=self.error_response(
                    bundle.request, {'errors': form.errors}))

        return bundle
