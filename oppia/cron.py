# Interpreter deliberately excluded here - set it in your cron shell script.
# /usr/bin/env python

import os, time, sys
import argparse, hashlib, subprocess

from django.conf import settings
from awards import courses_completed

def run(hours):
    print 'Starting OppiaMobile cron...'
    now = time.time()
    path = settings.COURSE_UPLOAD_DIR + "temp"
    print 'Cleaning up: ' + path
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.stat(f).st_mtime < now - 3600*6:
            print f
            if os.path.isfile(f):
                os.remove(f)
    

    courses_completed(int(hours))           
    print 'cron completed'


if __name__ == "__main__":
    import django
    django.setup()
    parser = argparse.ArgumentParser()
    parser.add_argument("hours", help="", default=0, nargs="?")
    args = parser.parse_args()
    run(args.hours) 
