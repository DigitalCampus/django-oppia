# oppia/content/views.py
import hashlib
import math
import os
import subprocess
import urllib
import uuid

from django import forms
from django.conf import settings
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.content.forms import VideoEmbedHelperForm


'''
Processes the video file found at the given URL and provides the embed code and sample images for embedding into Moodle.

NOTE: for this to run you will need to have ffmpeg and avprobe installed
For Ubuntu these can be installed by:

ffmpeg see: https://launchpad.net/~mc3man/+archive/ubuntu/trusty-media
avprobe: sudo apt-get install libav-tools

'''
def video_embed_helper(request):
    
    processed_video = None
    
    if request.method == 'POST':
        form = VideoEmbedHelperForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data.get("video_url")
            video_guid = str(uuid.uuid4())
            video_local_file = os.path.join(settings.COURSE_UPLOAD_DIR,'temp',video_guid)
            downloadError = None
            processed_video = {}

            # Need to add better validation here
            try:
                urllib.urlretrieve(video_url, filename=video_local_file)
            except IOError as err:
                downloadError = err
                processed_video['success'] = False
                processed_video['error'] = _("url_download_fail")

            if downloadError is None and can_execute("avprobe") and can_execute("ffmpeg"):

                # get the basic meta info
                embed_template = "[[media object='{\"filename\":\"%s\",\"download_url\":\"%s\",\"digest\":\"%s\", \"filesize\":%d, \"length\":%d}']]IMAGE/TEXT HERE[[/media]]"
                file_size = os.path.getsize(video_local_file)
                md5sum = md5_checksum(video_local_file)

                # get video length
                success, file_length = get_length(video_local_file)

                if success:
                    # create some image/screenshots
                    image_path = generate_video_screenshots(video_local_file, video_guid)
                    processed_video['embed_code'] = embed_template % (video_url.split('/')[-1], video_url, md5sum, file_size, file_length)

                    # Add the generated images to the output
                    processed_video['image_url_root'] = settings.MEDIA_URL + "temp/" +  video_guid + ".images/"
                    processed_video['image_files'] = next(os.walk(image_path))[2]
                    processed_video['success'] = True

                else:
                    processed_video['success'] = False
                    processed_video['error'] = _("get_length_error")

            else:
                processed_video['success'] = False
                if downloadError is not None:
                    processed_video['error'] = downloadError.strerror
                else:
                    processed_video['error'] = _("ffmpeg_missing")

            # try to delete the temp video file
            try:
                os.remove(video_local_file)
            except OSError:
                pass
    else:
        form = VideoEmbedHelperForm() 

    return render_to_response('oppia/content/video-embed-helper.html',  
                              {'settings': settings,
                               'form': form,
                               'processed_video': processed_video }, 
                              context_instance=RequestContext(request))
    
    
def get_length(filename):
    result = subprocess.Popen(["avprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

    duration_list = [x for x in result.stdout.readlines() if "Duration" in x]
    if len(duration_list) != 0:
        time_components = duration_list[0].split(',')[0].split(':')
        hours = int(time_components[1])
        mins = int(time_components[2])
        secs = math.floor(float(time_components[3]))
        video_length = (hours*60*60) + (mins*60) + secs
        return True, int(video_length)
    else:
        return False, 0

def generate_video_screenshots(video_local_file, video_guid):

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'temp')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'temp'))

    image_path = os.path.join(settings.MEDIA_ROOT, 'temp', video_guid + ".images")

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    IMAGE_WIDTH = 320
    IMAGE_HEIGHT = 180

    image_generator_command = "ffmpeg -i %s -r 0.02 -s %dx%d -f image2 %s/frame-%%03d.png" % (video_local_file, IMAGE_WIDTH, IMAGE_HEIGHT, image_path )
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

def md5_checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
