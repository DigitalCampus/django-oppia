from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext

from oppia.deviceadmin.models import UserDevice


def user_devices_list(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    devices = UserDevice.objects.all()

    return render_to_response('oppia/deviceadmin/list.html',
                              { 'devices': devices },
                              context_instance=RequestContext(request))