'''
 Checks the media download urls to ensure they are valid links

 For full instructions, see the documentation at
 https://oppiamobile.readthedocs.org/en/latest/
'''

import urllib
import time
import django.db.models

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from oppia.models import Media


class Command(BaseCommand):
    help = _(u"Checks the media download urls to ensure they are valid links")

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        media = Media.objects.all()
        for m in media:
            self.stdout.write("Checking: " + m.filename)
            try:
                response = urllib.request.urlopen(m.download_url)
                if m.filesize is not None:
                    total_size = int(response.getheader('content-length'))
                    if total_size != m.filesize:
                        self.stdout \
                            .write("INFO: file sizes appear to be different:")
                        self.stdout \
                            .write("filesize recorded in db:" + m.filesize)
                        self.stdout \
                            .write("filesize of download url:" + total_size)
            except urllib.error.HTTPError:
                self.stdout \
                    .write("WARNING: media file not found at: "
                           + m.download_url)
