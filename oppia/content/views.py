# oppia/content/views.py
import os
import urllib
import uuid

from django import forms
from django.conf import settings
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.content.forms import VideoEmbedHelperForm


def video_embed_helper(request):
    if request.method == 'POST':
        form = VideoEmbedHelperForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data.get("video_url")
            video_guid = str(uuid.uuid4())
            video_local_file = os.path.join(settings.COURSE_UPLOAD_DIR,'temp',video_guid)
            # Need to add better validation here
            try:
                urllib.urlretrieve(video_url, filename=video_local_file)
            except:
                pass
            
            
            
            # try to delete, 
            try:
                os.remove(video_local_file)
            except OSError:
                pass
            
    else:
        form = VideoEmbedHelperForm() 
    

    return render_to_response('oppia/content/video-embed-helper.html',  
                              {'settings': settings,
                               'form': form}, 
                              context_instance=RequestContext(request))