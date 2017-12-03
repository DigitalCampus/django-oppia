

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from oppia.api.publish import get_messages_array

from oppia.av import process_media

@csrf_exempt
def upload_view(request):
    
    # get the messages to clear possible previous unprocessed messages
    get_messages_array(request)

    if request.method != 'POST':
        return HttpResponse(status=405)

    
    required = ['username','password']

    validationErrors = []

    for field in required:
        if field not in request.POST:
            validationErrors.append("field '{0}' missing".format(field))

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
            
    if validationErrors:
        return JsonResponse({ 'errors' : validationErrors }, status=400, )  
   
    result = process_media.process(request, user)

    if result['result']:
        return HttpResponse(status=201)
    else:
        return JsonResponse({'messages': result['errors']}, status=400)
