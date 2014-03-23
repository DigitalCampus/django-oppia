'''
 Cleans up any old files in the oppia uploads directory

 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
'''

import os
import time 
import django.db.models
from django.conf import settings
from oppia.models import Course

def run():
    files = os.listdir(settings.COURSE_UPLOAD_DIR)
    for filename in files:
        if filename.endswith(".zip"):
            # find out if it's a live course file
            courses = Course.objects.filter(filename=filename)
            if courses.count() == 0:
                #delete the file
                os.remove(settings.COURSE_UPLOAD_DIR + filename)
                print "Removed: " + filename
                
if __name__ == "__main__":
    run()  