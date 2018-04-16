
# oppia/tracker/views.py

import json

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.tracker.forms import UploadTrackerForm

def upload_view(request):
    if not request.user.userprofile.get_can_upload_tracker():
        raise exceptions.PermissionDenied
    
    if request.method == 'POST':    
        form = UploadTrackerForm(request.POST,request.FILES)
        if form.is_valid():
            tracker_file = request.FILES["tracker_file"]
            
            #tracker_json = json.loads(tracker_file)
            
            return HttpResponseRedirect(reverse('oppia_tracker_upload_success'))
    else:
        form = UploadTrackerForm()

    return render(request, 'oppia/tracker/upload.html', 
                              {'form': form,
                               'title':_(u'Upload Activity Log')})
    
    
def upload_success_view(request):
    return render(request, 'oppia/tracker/upload_success.html', 
                              {'title':_(u'Upload Activity Log')})