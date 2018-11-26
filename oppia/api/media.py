# oppia/api/media.py

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from oppia.api.publish import get_messages_array
from oppia.av.models import UploadedMedia
from oppia.av import handler


@csrf_exempt
def upload_view(request):

    # get the messages to clear possible previous unprocessed messages
    get_messages_array(request)

    if request.method != 'POST':
        return HttpResponse(status=405)

    required = ['username', 'password']

    validation_errors = []

    for field in required:
        if field not in request.POST:
            validation_errors.append("field '{0}' missing".format(field))

    # authenticate user
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        messages.error(request, "Invalid username/password")
        response_data = {
            'message': _('Authentication errors'),
            'messages': get_messages_array(request)
        }
        return JsonResponse(response_data, status=401)

    if validation_errors:
        return JsonResponse({'errors': validation_errors}, status=400, )

    result = handler.upload(request, user)

    if result['result'] == UploadedMedia.UPLOAD_STATUS_SUCCESS:
        media = result['media']
        embed_code = media.get_embed_code(request.build_absolute_uri(media.file.url))

        return JsonResponse({'embed_code': embed_code}, status=201)
    else:
        response = {'messages': result['errors']}
        return JsonResponse(response, status=400)
