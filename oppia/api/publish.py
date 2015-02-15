# This is a workaround since Tastypie doesn't accept file Uploads
from django.conf import settings
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def publish_view(request):
    
    if request.method == 'POST':
        print "hello"
        # authenticate user
        if 'username' not in request.POST or 'password' not in request.POST:
            raise Http404
        print request.POST['username']
        print request.POST['password']
    else:
        raise Http404
    return render_to_response('oppia/server.html',  
                              {'settings': settings}, 
                              content_type="application/json", 
                              context_instance=RequestContext(request))