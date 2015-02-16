# This is a workaround since Tastypie doesn't accept file Uploads
import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from oppia.uploader import handle_uploaded_file
from django.contrib import messages

@csrf_exempt
def publish_view(request):
    
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    # authenticate user
    if 'username' not in request.POST or 'password' not in request.POST or 'course_file' not in request.FILES:
        return HttpResponse(status=400)
   
    # TODO - add tags & is_draft
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return HttpResponse(status=401)
            
    extract_path = os.path.join(settings.COURSE_UPLOAD_DIR,'temp',str(user.id))
    course = handle_uploaded_file(request.FILES['course_file'], extract_path, request, user)

    if course is False:
        return HttpResponse(status=500)
    else:
        return HttpResponse(status=201)
    