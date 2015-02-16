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
    
    if request.method is not 'POST':
        raise Http404
    
    # authenticate user
    if 'username' not in request.POST or 'password' not in request.POST:
        raise Http404
    
    if 'course_file' not in request.FILES:
        raise Http404
   
    # TODO - add tags & is_draft
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        raise Http404
            
    extract_path = os.path.join(settings.COURSE_UPLOAD_DIR,'temp',str(user.id))
    course = handle_uploaded_file(request.FILES['course_file'], extract_path, request, user)

    if course is False:
        raise Http404
   
    
        
    return render_to_response('oppia/server.html',  
                              {'settings': settings}, 
                              content_type="application/json", 
                              context_instance=RequestContext(request))