import os

from django.conf import settings
from django.core.management.base import BaseCommand

from oppia.models import Award


class Command(BaseCommand):
    help = 'Cleans certificate files - i.e. removes old certificate files \
            that are no longer valid'

    def handle(self, *args, **options):
        cert_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
        for root, dirs, files in os.walk(cert_dir):
            for name in files:
                full_path = os.path.join(root, name)

                # lookup the file in the award db
                relative_path = full_path.replace(
                    os.path.join(settings.MEDIA_ROOT, ''), '')
                try:
                    award = Award.objects.get(certificate_pdf=relative_path)
                    print("Found:  %s : %s" % (award, relative_path))
                except Award.DoesNotExist:
                    # delete award
                    print("Not found: %s" % relative_path)
                    os.remove(full_path)
                    print("%s deleted" % relative_path)
