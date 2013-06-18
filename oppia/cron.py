#!/usr/bin/env python
import os, time, sys
from django.conf import settings
from awards import *

def run():
    print 'Starting cron for courses'
    now = time.time()
    path = settings.COURSE_UPLOAD_DIR + "temp"
    for f in os.listdir(path):
        f = os.path.join(path, f)
        if os.stat(f).st_mtime < now - 3600*6:
            print f
            if os.path.isfile(f):
                os.remove(f)
     
    created_quizzes(10)
    courses_completed()           
    print 'Cron ended for courses'
    return

if __name__ == "__main__":
    run()