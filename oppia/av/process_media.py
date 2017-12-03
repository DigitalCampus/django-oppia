

import os, time, sys, math
import argparse, hashlib, subprocess

from django.conf import settings

def process(uploaded_media):
    
    media_full_path = os.path.join(settings.MEDIA_ROOT, uploaded_media.file.name)
    media_length = get_length(media_full_path)
    uploaded_media.length = media_length
    uploaded_media.save()
    
    
    
def get_length(filepath):
    result = subprocess.Popen(["avprobe", filepath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    duration_list = [x for x in result.stdout.readlines() if "Duration" in x]
    
    time_components = duration_list[0].split(',')[0].split(':')
    
    hours = int(time_components[1])
    mins = int(time_components[2])
    secs = math.floor(float(time_components[3]))
    
    return int((hours*60*60) + (mins*60) + secs)