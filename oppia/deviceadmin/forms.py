from gcm.forms import RegisterDeviceForm

from oppia.deviceadmin.models import UserDevice


class RegisterUserDeviceForm(RegisterDeviceForm):

     class Meta:
        model = UserDevice
        fields = ('dev_id', 'reg_id', 'name', 'model_name',)