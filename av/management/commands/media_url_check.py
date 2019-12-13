'''
 Checks the media download urls to ensure they are valid links
'''

import urllib

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from oppia.models import Media


class Command(BaseCommand):
    help = _(u"Checks the media download urls to ensure they are valid links")

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
            except Exception:
                self.stdout \
                    .write("WARNING: media file not found at: "
                           + m.download_url)
