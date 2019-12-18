from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, Unauthorized
from tastypie.resources import ModelResource

from api.serializers import UserJSONSerializer
from profile.forms import ProfileForm
from profile.models import UserProfile, CustomField, UserProfileCustomField

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
        if 'jobtitle' in bundle.data:
            user_profile.job_title = bundle.data['jobtitle']
        if 'organisation' in bundle.data:
            user_profile.organisation = bundle.data['organisation']
        if 'phoneno' in bundle.data:
            user_profile.phone_number = bundle.data['phoneno']
        user_profile.save()

    def process_profile_update_custom_fields(self, bundle):
        # Create any CustomField entries
        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            if (bundle.data[custom_field.id] is not None
                    and bundle.data[custom_field.id] != '') \
                    or custom_field.required is True:

                profile_field, created = UserProfileCustomField.objects \
                    .get_or_create(key_name=custom_field, user=bundle.obj)

                if custom_field.type == 'int':
                    profile_field.value_int = bundle.data[custom_field.id]
                elif custom_field.type == 'bool':
                    profile_field.value_bool = bundle.data[custom_field.id]
                else:
                    profile_field.value_str = bundle.data[custom_field.id]

                profile_field.save()

    def process_profile_update(self, bundle):
        data = {'email': bundle.data['email']
                if 'email' in bundle.data else '',
                'first_name': bundle.data['firstname'],
                'last_name': bundle.data['lastname'],
                'username': bundle.request.user}

        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            try:
                data[custom_field.id] = bundle.data[custom_field.id]
            except KeyError:
                pass

        profile_form = ProfileForm(data)
        if not profile_form.is_valid():
            str = ""
            for key, value in profile_form.errors.items():
                for error in value:
                    str += error + "\n"
            raise BadRequest(str)
        else:
            email = bundle.data['email'] if 'email' in bundle.data else ''
            first_name = bundle.data['firstname']
            last_name = bundle.data['lastname']

        try:
            bundle.obj = User.objects.get(username=bundle.request.user)
            bundle.obj.first_name = first_name
            bundle.obj.last_name = last_name
            bundle.obj.email = email
            bundle.obj.save()
        except User.DoesNotExist:
            raise BadRequest(_(u'Username not found'))

        # Create base UserProfile
        self.process_profile_update_base_profile(bundle)

        # Create any CustomField entries
        self.process_profile_update_custom_fields(bundle)
        
        return bundle
        
    def obj_create(self, bundle, **kwargs):
        required = ['firstname',
                    'lastname']
        check_required_params(bundle, required)

        # can't edit another users account
        if 'username' in bundle.data \
                and bundle.data['username'] != bundle.request.user:
            raise Unauthorized(_("You cannot edit another users profile"))

        bundle = self.process_profile_update(bundle)        
        return bundle
