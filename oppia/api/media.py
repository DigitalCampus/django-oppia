# oppia/api/media.py
import hashlib

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from oppia.av.models import UploadedMedia

@csrf_exempt
def media_upload_view(request):
    
    # get the messages to clear possible previous unprocessed messages
    get_messages_array(request)

    if request.method != 'POST':
        return HttpResponse(status=405)
    
    if validate_fields(request) == False:
        response_data = {
            'messages': get_messages_array(request)
        }
        print response_data
        return JsonResponse(response_data, status=400)
        
    # authenticate user
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        messages.error(request, "Invalid username/password")
        response_data = {
            'message': _('Authentication errors'),
            'messages': get_messages_array(request)
        }
        return JsonResponse(response_data, status=401)
     
    if settings.OPPIA_STAFF_ONLY_UPLOAD is True \
            and not user.is_staff \
            and user.userprofile.can_upload is False:
        return HttpResponse(status=401)
    
    uploaded_media = UploadedMedia(create_user = user, update_user = user)
    uploaded_media.file = request.FILES["media_file"]
    uploaded_media.save()
    
    # generate the md5 and save this
    uploaded_media.md5 = hashlib.md5(open(uploaded_media.file.path, 'rb').read()).hexdigest()
    uploaded_media.save()
    
    if request.FILES.has_key('media_image'):
        uploaded_media.image = request.FILES["media_image"]
        uploaded_media.save()
    
    return HttpResponse(status=201)
    
def validate_fields(request):
    required = ['username','password', 'course_shortname']
    is_valid = True

    for r in required:
        if r not in request.POST:
            print r + " not found"
            messages.error(request, _("required field '%s' not found") % r)
            is_valid = False

    if 'media_file' not in request.FILES:
        print "Media file not found"
        messages.error(request, _("Media file not found"))
        is_valid = False
    else:
        media_file = request.FILES['media_file']
        if media_file is None:
            is_valid = False

    return is_valid
    
def get_messages_array(request):
    msgs = messages.get_messages(request)
    response = []
    for msg in msgs:
        response.append({'tags': msg.tags, 'message': msg.message })
    return response