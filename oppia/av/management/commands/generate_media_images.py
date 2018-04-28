# coding: utf-8

"""
Management command to generate sample media images
"""
import os
import subprocess
import time 

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from oppia.av.models import UploadedMedia, UploadedMediaImage

DEFAULT_WIDTH = 320
DEFAULT_HEIGHT = 180

class Command(BaseCommand):
    help = _(u"Generates sample media images")


    def add_arguments(self, parser):
        pass
        

    def handle(self, *args, **options):
        """
        Generates sample media images
        """
        media = UploadedMedia.objects.filter(uploadedmediaimage__isnull=True)
           
        for m in media:
            print m.file.path
            
            cache_dir = os.path.join(settings.MEDIA_ROOT, "cache", "temp", os.path.basename(m.file.name))
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
                print "  > Created output dir " + cache_dir
            
            print "  > Generating miniatures... \r",
            image_generator_command = "ffmpeg -i %s -r 0.02 -s %dx%d -f image2 %s/frame-%%03d.png" % (m.file.path, DEFAULT_WIDTH, DEFAULT_HEIGHT, cache_dir)
            ffmpeg = subprocess.Popen(image_generator_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
            currentFrame = 0
            for line in iter(ffmpeg.stdout.readline,''):
                if "frame=" in line:
                    if line.split(" ")[3] is "":
                        frame = int(line.split(" ")[4])
                    else:
                        frame = int(line.split(" ")[3])
                    if frame > currentFrame:
                        currentFrame = frame
                        print "  > Generating miniatures... " + str(frame*10) + "% \r",
            print "  > Generating miniatures... 100% \r\n",
        
            # Now get the images generated and add to the db
            image_file_list = os.listdir(cache_dir)
            for filename in image_file_list:
                print filename
                media_image = UploadedMediaImage(create_user=m.create_user, uploaded_media=m)
                data = None
                with open(os.path.join(cache_dir,filename),'rb') as f:
                    data = f.read()
                media_image.image.save(filename, ContentFile(data))
                media_image.save()
        
        print "\n  > Process completed."
            
        
        
        