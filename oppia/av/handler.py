
import os
import time
import sys
import math
import argparse
import hashlib
import subprocess

from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from oppia.av.forms import UploadMediaForm
from oppia.av.models import UploadedMedia
from oppia.api.publish import get_messages_array


def upload(request, user):

    form = UploadMediaForm(request.POST, request.FILES, request=request)
    if form.is_valid():
        uploaded_media = UploadedMedia(create_user=user,
                                      update_user=user, )
        uploaded_media.file = request.FILES["media_file"]
        uploaded_media.save()
        md5 = hashlib.md5(open(uploaded_media.file.path, 'rb').read()).hexdigest()
        uploaded_media.md5 = md5
        uploaded_media.save()

        try:
            media_full_path = os.path.join(settings.MEDIA_ROOT, uploaded_media.file.name)
            media_length = get_length(media_full_path)
            uploaded_media.length = media_length
            uploaded_media.save()
        except OSError:
            '''
            likely means avprobe/'libav-tools' is not installed
            '''
            uploaded_media.delete()
            messages.add_message(request, messages.ERROR, _(u"The avprobe/libav-tools package might not be installed on this server. Please ask your Oppia system administrator to install it for you (`apt-get install libav-tools`)."), "danger")
            return {'result': UploadedMedia.UPLOAD_STATUS_FAILURE, 'form': form, 'errors': _(u"The avprobe/libav-tools package might not be installed on this server.")}

        return {'result': UploadedMedia.UPLOAD_STATUS_SUCCESS, 'media': uploaded_media}
    else:

        errors = []
        for field, error in form.errors.items():
            for e in error:
                errors.append(e)
        return {'result': UploadedMedia.UPLOAD_STATUS_FAILURE, 'form': form, 'errors': errors}

    
def get_length(filepath):
    result = subprocess.Popen(["avprobe", filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration_list = [x for x in result.stdout.readlines() if "Duration" in x]

    time_components = duration_list[0].split(',')[0].split(':')

    hours = int(time_components[1])
    mins = int(time_components[2])
    secs = math.floor(float(time_components[3]))

    return int((hours * 60 * 60) + (mins * 60) + secs)
