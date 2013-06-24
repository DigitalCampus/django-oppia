# Interpreter deliberately excluded here - set it in your cron shell script.
# /usr/bin/env python

import os, time, sys
from django.conf import settings
from awards import created_quizzes, courses_completed
from django.core.mail import send_mail

def run():
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
    
    print 'Awarding badges...'
    created_quizzes(10)
    courses_completed()           
    print 'cron completed'
    #send_mail('OppiaMobile: cron complete', 'cron completed', 
    #    settings.SERVER_EMAIL, [settings.SERVER_EMAIL], fail_silently=False)

if __name__ == "__main__":
    run()
