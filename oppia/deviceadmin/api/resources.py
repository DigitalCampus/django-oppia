# oppia/deviceadmin/api/resources.py
from gcm.resources import DeviceResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization

from oppia.deviceadmin.forms import RegisterUserDeviceForm
from oppia.deviceadmin.models import UserDevice


class UserDeviceResource(DeviceResource):

    register_form_class = RegisterUserDeviceForm

    class Meta(DeviceResource.Meta):
        resource_name = 'device'
        queryset = UserDevice.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        allowed_methods = ['post']

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super(UserDeviceResource, self).form_valid(form)
