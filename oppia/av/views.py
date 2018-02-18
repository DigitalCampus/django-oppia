# oppia/av/views.py
import datetime


from django.conf import settings
from django.core import exceptions
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.av.forms import UploadMediaForm
from oppia.av.models import UploadedMedia
from oppia.av import handler

def home_view(request):
    uploaded_media = UploadedMedia.objects.all()

    return render(request, 'oppia/av/home.html', 
                              { 'title':_(u'Uploaded Media'),
                                'uploaded_media': uploaded_media })

def upload_view(request):
    if not request.user.userprofile.get_can_upload():
        raise exceptions.PermissionDenied
    
    if request.method == 'POST':    
       result = handler.upload(request, request.user)
       
       if result['result'] == UploadedMedia.UPLOAD_STATUS_SUCCESS:
           return HttpResponseRedirect(reverse('oppia_av_upload_success', args=[result['media'].id]))
       else:
           form = result['form']
               
    else:
        form = UploadMediaForm() # An unbound form

    return render(request, 'oppia/av/upload.html', 
                              {'form': form,
                               'title':_(u'Upload Media')})
    
def upload_success_view(request,id):
     media = get_object_or_404(UploadedMedia, pk=id)
     
     embed_code = media.get_embed_code(request.build_absolute_uri(media.file.url))
     
     return render(request, 'oppia/av/upload_success.html', 
                              {'title':_(u'Upload Media'),
                               'media': media,
                               'embed_code': embed_code })
     
     
    