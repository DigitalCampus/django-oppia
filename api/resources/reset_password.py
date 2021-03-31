
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from api.utils import check_required_params


class ResetPasswordResource(ModelResource):
    '''
    For resetting user password
    '''
    message = fields.CharField()

    class Meta:
        queryset = User.objects.all()
        resource_name = 'reset'
        allowed_methods = ['post']
        fields = ['message']
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):
        required = ['username', ]
        check_required_params(bundle, required)

        username = bundle.data['username']
        # find if username or email address
        user = User.objects.filter(Q(username=username) | 
                                   Q(email__iexact=username)).first()

        if user is not None:
            prf = PasswordResetForm({'email': user.email})
            if prf.is_valid():
                prf.get_users(user.email)
                prf.save(request=bundle.request,
                         from_email=settings.SERVER_EMAIL,
                         use_https=bundle.request.is_secure())

        return bundle

    def dehydrate_message(self, bundle):
        message = _(u'An email has been sent to your email address, please follow the instructions to reset your password.')
        return message
