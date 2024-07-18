import os.path
from shutil import copyfile

from django.conf import settings
from django.core.management.base import BaseCommand

from av.models import UploadedMedia

class Command(BaseCommand):
    help = 'To sync externally hosted courses/media'

    def handle(self, *args, **options):
        if not settings.OPPIA_EXTERNAL_STORAGE:
            print("Exiting as this instance of Oppia server is not configured for external storage")
            return

        # Sync media
        uploaded_media = UploadedMedia.objects.all()
        for um in uploaded_media:
            print("checking %s" % um.filename())
            source_full_path = os.path.join(settings.MEDIA_ROOT, um.file.name)
            external_full_path = os.path.join(settings.OPPIA_EXTERNAL_STORAGE_MEDIA_ROOT, um.filename())
            if not os.path.isfile(external_full_path):
                copyfile(source_full_path, external_full_path)
                print("copied to %s" % external_full_path)
            else:
                print("File already synced")