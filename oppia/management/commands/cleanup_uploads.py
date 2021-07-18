# coding: utf-8

"""
Management command to clean up any old files in the oppia uploads directory
"""
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from oppia.models import Course


class Command(BaseCommand):
    help = "Cleans up any old files in the oppia uploads and courses directory"

    def handle(self, *args, **options):
        self.remove_no_matching_courses()
        self.remove_courses_no_file()
        self.remove_old_expanded_folders()

    def remove_no_matching_courses(self):
        """
        Remove files that don't have matching courses
        """
        files = os.listdir(settings.COURSE_UPLOAD_DIR)
        for filename in files:
            if filename.endswith(".zip"):
                # find out if it's a live course file
                courses = Course.objects.filter(filename=filename)
                if courses.count() == 0:
                    # delete the file
                    os.remove(os.path.join(settings.COURSE_UPLOAD_DIR,
                                           filename))
                    self.stdout.write("Removed: " + filename)

    def remove_courses_no_file(self):
        """
        Flag up courses that don't have files
        """
        courses = Course.objects.all()
        for course in courses:
            if not os.path.isfile(os.path.join(settings.COURSE_UPLOAD_DIR,
                                               course.filename)):
                self.stdout \
                    .write("FILE MISSING: %s for %s " % (course.filename,
                                                         course.title))

    def remove_old_expanded_folders(self):
        """
        Remove old expanded folders from media/courses
        """
        try:
            files = os.listdir(os.path.join(settings.MEDIA_ROOT, 'courses'))
            for filename in files:
                if os.path.isdir(
                        os.path.join(settings.MEDIA_ROOT,
                                     'courses',
                                     filename)):
                    courses = Course.objects.filter(shortname=filename)
                    if courses.count() == 0:
                        shutil.rmtree(os.path.join(settings.MEDIA_ROOT,
                                                   'courses',
                                                   filename))
                        self.stdout.write("Removed: " + filename)
        except FileNotFoundError:  # dir doesn;t exsit
            pass
