from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from profile.views import manage


class DeleteAccountResource(ModelResource):

    message = fields.CharField(readonly=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'deleteaccount'
        allowed_methods = ['post']
        fields = []
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):

        if 'password' not in bundle.data:
            raise BadRequest(_(u'Password missing'))

        username = bundle.request.user.username
        password = bundle.data['password']

        u = authenticate(username=username, password=password)
        if u is not None:
            # continue with deletion
            manage.delete_user_data(u)
        else:
            raise BadRequest(_(u'Authentication failure'))

        del bundle.data['password']  # don't send password back

        return bundle

    def dehydrate_message(self, bundle):
        return _(u'Your account has now been deleted')
