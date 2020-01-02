
from oppia.test import OppiaTestCase
from av.models import UploadedMedia, UploadedMediaImage


class AVModelsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_av_uploadedmedia.json']

    def test_uploadedmedia_str(self):
        um = UploadedMedia.objects.get(pk=1)
        self.assertEqual(
            'uploaded/2018/02/ldrshp-mgmt-unit-2-risk-mgmt-D-v2.m4v',
            str(um))

    def test_uploadedmediaimage_str(self):
        um = UploadedMediaImage.objects.get(pk=1)
        self.assertEqual(
            'uploaded/images/fr/am/frame-001_71mRFnT.png',
            str(um))