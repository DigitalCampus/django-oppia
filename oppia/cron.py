# Interpreter deliberately excluded here - set it in your cron shell script.
# /usr/bin/env python

import os
import time
import sys
import argparse
import hashlib
import subprocess

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from settings.models import SettingProperties

def run(hours):
    print('Starting OppiaMobile cron...')
    oppia_cron(hours)
    print('cron completed')

def oppia_cron(hours=0):   
    
    #check if cron already running
    prop, created = SettingProperties.objects.get_or_create(key='oppia_cron_lock',int_value=1)
    if not created:
        print("Oppia cron is already running")
        return
    
     
    now = time.time()
    path = os.path.join(settings.COURSE_UPLOAD_DIR, "temp")

    if os.path.exists(path):
        print('Cleaning up: ' + path)
        for f in os.listdir(path):
            f = os.path.join(path, f)
            if os.stat(f).st_mtime < now - 3600 * 6:
                print("deleting: {file}".format(file=f))
                if os.path.isfile(f):
                    os.remove(f)
    else:
        print('{path} does not exist. Don\'t need to clean it'.format(path=path))

    from awards import courses_completed
    courses_completed(int(hours))

    # create and new media images
    call_command('generate_media_images')
    
    SettingProperties.set_string('oppia_cron_last_run', timezone.now())
    SettingProperties.delete_key('oppia_cron_lock')

if __name__ == "__main__":
    import django
    django.setup()
    parser = argparse.ArgumentParser()
    parser.add_argument("hours", help="", default=0, nargs="?")
    args = parser.parse_args()
    run(args.hours)
