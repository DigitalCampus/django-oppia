# oppia/av/views.py
import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.av.forms import UploadMediaForm

def upload_view(request):
    if not request.user.userprofile.get_can_upload():
        return HttpResponse('Unauthorized', status=401)
    
    if request.method == 'POST':
        form = UploadMediaForm(request.POST,request.FILES)
        if form.is_valid(): # All validation rules pass
           pass
    else:
        form = UploadMediaForm() # An unbound form

    return render_to_response('oppia/av/upload.html', 
                              {'form': form,
                               'title':_(u'Upload Media')},
                              context_instance=RequestContext(request))
    