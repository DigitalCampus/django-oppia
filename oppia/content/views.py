# oppia/content/views.py
import hashlib
import math
import os
import subprocess
import urllib
import uuid
import oppia.content

from django import forms
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.content.forms import MediaEmbedHelperForm

'''
Processes the media file found at the given URL and provides the embed code and sample images for embedding into Moodle.

NOTE: for this to run you will need to have ffmpeg and avprobe installed
For Ubuntu these can be installed by:

ffmpeg see: https://launchpad.net/~mc3man/+archive/ubuntu/trusty-media
avprobe: sudo apt-get install libav-tools

'''


def media_embed_helper(request):

    processed_media = None

    if request.method == 'POST':
        form = MediaEmbedHelperForm(request.POST)
        if form.is_valid():
            media_url = form.cleaned_data.get("media_url")
            media_guid = str(uuid.uuid4())
            media_local_file = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', media_guid)
            download_error = None
            processed_media = {}

            # Need to add better validation here
            download_error, processed_media = check_media_link(media_url, media_local_file, download_error, processed_media)

            download_error, processed_media = process_media_file(media_local_file, download_error, processed_media)
            
            # try to delete the temp media file
            try:
                os.remove(media_local_file)
            except OSError:
                pass
    else:
        form = MediaEmbedHelperForm()

    return render(request, 'oppia/content/media-embed-helper.html',
                              {'settings': settings,
                               'form': form,
                               'processed_media': processed_media})


def process_media_file(media_local_file, download_error, processed_media):
    if download_error is None and can_execute("avprobe") and can_execute("ffmpeg"):

        # get the basic meta info
        file_size = os.path.getsize(media_local_file)
        md5sum = md5_checksum(media_local_file)

        # get media length
        success, file_length = get_length(media_local_file)

        if success:
            # create some image/screenshots
            image_path = generate_media_screenshots(media_local_file, media_guid)
            processed_media['embed_code'] = oppia.content.EMBED_TEMPLATE % (media_url.split('/')[-1], media_url, md5sum, file_size, file_length)

            # Add the generated images to the output
            processed_media['image_url_root'] = settings.MEDIA_URL + "temp/" + media_guid + ".images/"
            processed_media['image_files'] = next(os.walk(image_path))[2]
            processed_media['success'] = True

        else:
            processed_media['success'] = False
            processed_media['error'] = _("get_length_error")

    else:
        processed_media['success'] = False
        if download_error is not None:
            processed_media['error'] = download_error.strerror
        else:
            processed_media['error'] = _("ffmpeg_missing")
    
    return download_error, processed_media

def check_media_link(media_url, media_local_file, download_error, processed_media):
    try:
        urllib.urlretrieve(media_url, filename=media_local_file)
    except IOError as err:
        download_error = err
        processed_media['success'] = False
        processed_media['error'] = _("url_download_fail")
    return download_error, processed_media

def get_length(filename):
    result = subprocess.Popen(["avprobe", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    duration_list = [x for x in result.stdout.readlines() if "Duration" in x]
    if len(duration_list) != 0:
        time_components = duration_list[0].split(',')[0].split(':')
        hours = int(time_components[1])
        mins = int(time_components[2])
        secs = math.floor(float(time_components[3]))
        media_length = (hours * 60 * 60) + (mins * 60) + secs
        return True, int(media_length)
    else:
        return False, 0


def generate_media_screenshots(media_local_file, media_guid):

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'temp')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'temp'))

    image_path = os.path.join(settings.MEDIA_ROOT, 'temp', media_guid + ".images")

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    image_generator_command = "ffmpeg -i %s -r 0.02 -s %dx%d -f image2 %s/frame-%%03d.png" % (media_local_file, oppia.content.SCREENSHOT_IMAGE_WIDTH, oppia.content.SCREENSHOT_IMAGE_HEIGHT, image_path)
    subprocess.call(image_generator_command, shell=True)
    return image_path


def can_execute(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return True

    return False


def md5_checksum(file_path):
    with open(file_path, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
