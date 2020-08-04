from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, Unauthorized
from tastypie.resources import ModelResource

from api.serializers import UserJSONSerializer
from profile.forms import ProfileForm
from profile.models import UserProfile, CustomField

from api.utils import check_required_params


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

        profile_form = ProfileForm(data)
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
            bundle.obj = User.objects.get(username=bundle.request.user)
            bundle.obj.first_name = first_name
            bundle.obj.last_name = last_name
            bundle.obj.email = email
            bundle.obj.save()
        except User.DoesNotExist:
            raise BadRequest(_(u'Username not found'))

        # Create base UserProfile
        user_profile = self.process_profile_update_base_profile(bundle)
        # Create any CustomField entries
        user_profile.update_customfields(bundle.data)

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
