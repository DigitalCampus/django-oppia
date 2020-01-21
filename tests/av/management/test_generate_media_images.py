import pytest

from av.models import UploadedMediaImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.urls import reverse
from oppia.test import OppiaTestCase


class GenerateMediaImagesTest(OppiaTestCase):

    media_file_path = './oppia/fixtures/reference_files/sample_video.m4v'

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_media_image(self):
        # upload a media file
        with open(self.media_file_path, 'rb') as media_file_content:
            media_file = SimpleUploadedFile(media_file_content.name,
                                            media_file_content.read(),
                                            content_type="video/m4v")

        self.client.force_login(self.admin_user)
        self.client.post(reverse('oppia_av_upload'),
                         {'media_file': media_file})

        image_count_start = UploadedMediaImage.objects.all().count()
        # run the generate_media_images command
        call_command('generate_media_images')

        image_count_end = UploadedMediaImage.objects.all().count()
        self.assertEqual(image_count_start+2, image_count_end)
