import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response

from django.template import RequestContext

from oppia.deviceadmin.forms import AdminMessageForm
from oppia.deviceadmin.models import UserDevice


def user_devices_list(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    devices = UserDevice.objects.all().order_by('-modified_date')

    return render_to_response('oppia/deviceadmin/list.html',
                              { 'devices': devices },
                              context_instance=RequestContext(request))

def send_message_to_device(request):

    if request.method != 'POST':
        return HttpResponse(status=405)

    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    form = AdminMessageForm(request.POST)
    if form.is_valid():
        action = form.cleaned_data.get("action")
        device_id = form.cleaned_data.get("device")

        message_data = {'type': 'admin', 'action': action}

        if 'password' in request.POST:
            password = request.POST.get('password')
            message_data['password'] = password

        device = UserDevice.objects.get(dev_id=device_id)
        message = device.send_message(message_data)
        print message # returns a tuple containing reg_ids as list and response json

        #return the response object as json
        return JsonResponse(json.dumps(message[1]))

    else:
        return HttpResponse(status=400)