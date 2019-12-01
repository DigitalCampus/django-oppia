from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tastypie import fields
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.exceptions import BadRequest, Unauthorized
from tastypie.models import ApiKey
from tastypie.resources import ModelResource

from tastypie.utils import trailing_slash, timezone
from tastypie.validation import Validation

from api.serializers import UserJSONSerializer
from profile.forms import ProfileForm
from profile.models import UserProfile, CustomField, UserProfileCustomField

from settings import constants
from settings.models import SettingProperties

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

    def obj_create(self, bundle, **kwargs):
        required = ['firstname',
                    'lastname']
        check_required_params(bundle, required)

        # can't edit another users account
        if 'username' in bundle.data \
                and bundle.data['username'] != bundle.request.user:
            raise Unauthorized(_("You cannot edit another users profile"))
        
        data = {'email': bundle.data['email'] if 'email' in bundle.data else '',
                'first_name': bundle.data['firstname'],
                'last_name': bundle.data['lastname'], 
                'username': bundle.request.user}

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
        
        user_profile, created = UserProfile.objects.get_or_create(user=bundle.obj)
        if 'jobtitle' in bundle.data:
            user_profile.job_title = bundle.data['jobtitle']
        if 'organisation' in bundle.data:
            user_profile.organisation = bundle.data['organisation']
        if 'phoneno' in bundle.data:
            user_profile.phone_number = bundle.data['phoneno']
        user_profile.save()
        return bundle