from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from settings import constants
from settings.models import SettingProperties


@method_decorator(staff_member_required, name='dispatch')
class MapView(TemplateView):

    def get(self, request):
        if SettingProperties.get_bool(
                constants.OPPIA_MAP_VISUALISATION_ENABLED, False):
            return render(request, 'reports/map.html')
        else:
            raise Http404()
