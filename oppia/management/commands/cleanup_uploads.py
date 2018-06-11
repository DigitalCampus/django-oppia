# coding: utf-8

"""
Management command to clean up any old files in the oppia uploads directory
"""
import os
import time
import django.db.models
import oppia.management.commands

from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum

from oppia.models import Course

class Command(BaseCommand):
    help = "Cleans up any old files in the oppia uploads directory"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Remove files that don't have matching courses
        """
        files = os.listdir(settings.COURSE_UPLOAD_DIR)
        for filename in files:
            if filename.endswith(".zip"):
                # find out if it's a live course file
                courses = Course.objects.filter(filename=filename)
                if courses.count() == 0:
                    #delete the file
                    os.remove(settings.COURSE_UPLOAD_DIR + filename)
                    print("Removed: " + filename)

        """
        Flag up courses that don't have files
        """
        courses = Course.objects.all()
        for course in courses:
            if not os.path.isfile(os.path.join(settings.COURSE_UPLOAD_DIR, course.filename)):
                print("FILE MISSING: %s for %s " % (course.filename, course.title))
