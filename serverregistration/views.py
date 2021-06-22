
from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.generic import FormView

from helpers.mixins.TitleViewMixin import TitleViewMixin

from settings import constants
from settings.models import SettingProperties
from serverregistration.forms import RegisterServerForm

class RegisterServerView(FormView, TitleViewMixin):
                         
    template_name = 'serverregistration/register.html'
    form_class = RegisterServerForm
    success_url = 'thanks/'
    title = _(u'Register Server')
    
    def get_initial(self):
        initial = {'server_url': SettingProperties.get_property(
            constants.OPPIA_HOSTNAME, ''),
                   }
        return initial