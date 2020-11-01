
import hashlib
import math
import os
import subprocess
import zipfile

from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from av import constants
from av.forms import UploadMediaForm
from av.models import UploadedMedia


def upload(request, user):

    form = UploadMediaForm(request.POST, request.FILES, request=request)
    if form.is_valid():
        uploaded_media = UploadedMedia(create_user=user, update_user=user)
        uploaded_media.file = request.FILES["media_file"]
        uploaded_media.save()
        file = open(uploaded_media.file.path, 'rb')
        md5 = hashlib.md5(file.read()).hexdigest()
        file.close()
        uploaded_media.md5 = md5
        uploaded_media.save()

        try:
            media_full_path = os.path.join(settings.MEDIA_ROOT,
                                           uploaded_media.file.name)
            media_length, result = get_length(media_full_path)
            if result:
                uploaded_media.length = media_length
                uploaded_media.save()
            else:
                uploaded_media.delete()
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(u"Corrupted media file"), "danger")
                return {'result': constants.UPLOAD_MEDIA_STATUS_FAILURE,
                        'form': form,
                        'errors': _(u"Corrupted media file")}
        except OSError:
            '''
            most likely means settings.MEDIA_PROCESSOR_PROGRAM is not installed
            '''
            uploaded_media.delete()
            messages.add_message(
                request,
                messages.ERROR,
                _(u"The %s program does not seem to be \
                  installed on this server, or is \
                  incorrectly configured. Please ask your \
                  Oppia system administrator to install it \
                  for you.") % settings.MEDIA_PROCESSOR_PROGRAM, "danger")
            return {'result': constants.UPLOAD_MEDIA_STATUS_FAILURE,
                    'form': form,
                    'errors':
                        _(u"The %s program might not be installed on \
                          this server.") % settings.MEDIA_PROCESSOR_PROGRAM}

        return {'result': constants.UPLOAD_MEDIA_STATUS_SUCCESS,
                'media': uploaded_media}
    else:

        errors = []
        for field, error in form.errors.items():
            for e in error:
                errors.append(e)
        return {'result': constants.UPLOAD_MEDIA_STATUS_FAILURE,
                'form': form,
                'errors': errors}


def get_length(filepath):
    with subprocess.Popen([settings.MEDIA_PROCESSOR_PROGRAM, filepath],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          encoding='utf8') as result:
        duration_list = [x for x in result.stdout.readlines()
                         if "Duration" in x]

    try:
        time_components = duration_list[0].split(',')[0].split(':')
        hours = int(time_components[1])
        mins = int(time_components[2])
        secs = math.floor(float(time_components[3]))
    except ValueError:
        return 0, False

    return int((hours * 60 * 60) + (mins * 60) + secs), True


def zip_course_media(zipname, media_contents):

    files = []

    for media in media_contents:
        if media.file and media.file.storage.exists(media.file.name):
            files.append(media.file)
            # zip.writestr(course.shortname + "/tracker.xml",
            # Tracker.to_xml_string(course, request.user))

    if len(files) == 0:
        return False

    path = os.path.join(settings.COURSE_UPLOAD_DIR, "temp", zipname)
    with zipfile.ZipFile(path, "w") as zip:
        for file in files:
            upload, filename = os.path.split(file.name)
            print(file.path)
            zip.write(file.path, filename)

    return path
