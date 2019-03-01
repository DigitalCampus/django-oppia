import os
import time
import sys
import argparse
import hashlib
import subprocess

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from settings.models import SettingProperties

class Command(BaseCommand):
    help = 'OppiaMobile cron command'

    def add_arguments(self, parser):

        # Optional argument to start the summary calculation from the beginning
        parser.add_argument(
            '--hours',
            dest='hours',
            help='no hours',
        )        
        
    def handle(self, *args, **options):
        if options['hours']:
            hours=options['hours']
        else:
            hours=0 
            
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
    
        from oppia.awards import courses_completed
        courses_completed(int(hours))
    
        # create and new media images
        call_command('generate_media_images')
        
        SettingProperties.set_string('oppia_cron_last_run', timezone.now())
        SettingProperties.delete_key('oppia_cron_lock')
            
            
    