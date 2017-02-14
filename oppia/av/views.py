# oppia/av/views.py
import datetime
import hashlib

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.av.forms import UploadMediaForm
from oppia.av.models import UploadedMedia

def upload_view(request):
    if not request.user.userprofile.get_can_upload():
        return HttpResponse('Unauthorized', status=401)
    
    if request.method == 'POST':
        form = UploadMediaForm(request.POST,request.FILES)
        if form.is_valid(): # All validation rules pass
           course_shortname = form.cleaned_data.get("course_shortname")
           length = form.cleaned_data.get("length")
           
           uploaded_media = UploadedMedia(create_user = request.user,
                                              update_user = request.user,
                                              course_shortname = course_shortname,
                                              length = length)
           if request.FILES.has_key('media_file'):
               uploaded_media.file = request.FILES["media_file"]
               uploaded_media.save()
               # generate the md5 and save this
               uploaded_media.md5 = hashlib.md5(open(uploaded_media.file.path, 'rb').read()).hexdigest()
               uploaded_media.save()
               
           if request.FILES.has_key('image_file'):
               uploaded_media.image = request.FILES["image_file"]
           uploaded_media.save()
           
           return HttpResponseRedirect(reverse('oppia_av_upload_success', args=[uploaded_media.id]))
               
    else:
        form = UploadMediaForm() # An unbound form

    return render_to_response('oppia/av/upload.html', 
                              {'form': form,
                               'title':_(u'Upload Media')},
                              context_instance=RequestContext(request))
    
def upload_success_view(request,id):
     media = get_object_or_404(UploadedMedia, pk=id)
     
     return render_to_response('oppia/av/upload_success.html', 
                              {'title':_(u'Upload Media'),
                               'media': media},
                              context_instance=RequestContext(request))
    