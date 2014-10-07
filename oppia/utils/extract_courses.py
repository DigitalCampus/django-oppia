'''
 Script to extract all current courses to media/courses dir
 
 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
'''
import os
import time 
import zipfile

import django.db.models

from django.conf import settings
from oppia.models import Course

def run():
    courses = Course.objects.all()
    for c in courses:
        zip = zipfile.ZipFile(settings.COURSE_UPLOAD_DIR + c.filename)
        zip.extractall(path=settings.MEDIA_ROOT + "courses/") 

if __name__ == "__main__":
    run()  