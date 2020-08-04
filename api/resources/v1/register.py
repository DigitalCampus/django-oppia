from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from tastypie.exceptions import BadRequest
from tastypie.models import ApiKey

from oppia import DEFAULT_IP_ADDRESS
from oppia.models import Tracker
from profile.forms import RegisterForm
from profile.models import CustomField

from settings import constants
from settings.models import SettingProperties

from api.utils import check_required_params

from api.resources.base_register import RegisterBaseResource


class RegisterResource(RegisterBaseResource):

    def obj_create(self, bundle, **kwargs):
        self_register = SettingProperties \
            .get_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                      settings.OPPIA_ALLOW_SELF_REGISTRATION)
        if not self_register:
            raise BadRequest(_(u'Registration is disabled on this server.'))
        required = ['username',
                    'password',
                    'passwordagain',
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
            error_str = ""
            for key, value in rf.errors.items():
                for error in value:
                    error_str += error + "\n"
            raise BadRequest(error_str)
        else:
            username = bundle.data['username']
            password = bundle.data['password']
            email = bundle.data['email'] if 'email' in bundle.data else '',
            first_name = bundle.data['firstname']
            last_name = bundle.data['lastname']

        try:
            bundle.obj = User.objects.create_user(username=username,
                                                  password=password)
            bundle.obj.first_name = first_name
            bundle.obj.email = email
            bundle.obj.last_name = last_name
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest(
                _(u'Username "%s" already in use, please select another'
                  % username))

        self.process_register_base_profile(bundle)

        self.process_register_custom_fields(bundle)

        u = authenticate(username=username, password=password)
        if u is not None and u.is_active:
            login(bundle.request, u)
            # Add to tracker
            tracker = Tracker()
            tracker.user = u
            tracker.type = 'register'
            tracker.ip = bundle.request.META.get('REMOTE_ADDR',
                                                 DEFAULT_IP_ADDRESS)
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
