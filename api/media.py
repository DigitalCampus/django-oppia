# oppia/api/media.py

from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from api.publish import get_messages_array
from av import handler
from av.models import UploadedMedia


def api_authenticate(request):
    required = ['username', 'password']

    validation_errors = []

    for field in required:
        if field not in request.POST:
            validation_errors.append("field '{0}' missing".format(field))

    if len(validation_errors) > 0:
        return False, \
            JsonResponse({'errors': validation_errors}, status=400), \
            None

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
        return False, JsonResponse(response_data, status=401), None
    else:
        return True, None, user


@csrf_exempt
def get_view(request, digest):
    get_messages_array(request)

    media = get_object_or_404(UploadedMedia, md5=digest)

    embed_code = media.get_embed_code(
        request.build_absolute_uri(media.file.url))
    resp_obj = {'embed_code': embed_code,
                'digest': media.md5,
                'filesize': media.get_filesize(),
                'download_url': request.build_absolute_uri(media.file.url),
                'length': media.length}
    return JsonResponse(resp_obj, status=200)


@csrf_exempt
def upload_view(request):

    # get the messages to clear possible previous unprocessed messages
    get_messages_array(request)

    if request.method != 'POST':
        return HttpResponse(status=405)

    valid, error, user = api_authenticate(request)
    if not valid:
        return error

    result = handler.upload(request, user)

    if result['result'] == UploadedMedia.UPLOAD_STATUS_SUCCESS:
        media = result['media']
        embed_code = media.get_embed_code(
            request.build_absolute_uri(media.file.url))

        return JsonResponse({'embed_code': embed_code,
                             'digest': media.md5,
                             'filesize': media.get_filesize(),
                             'download_url': request.build_absolute_uri(
                                 media.file.url)}, status=201)
    else:
        response = {'messages': result['errors']}
        return JsonResponse(response, status=400)
