
from oppia.test import OppiaTestCase
from av.models import UploadedMedia


class AVModelsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_av_uploadedmedia.json',
                'tests/test_course_permissions.json']

    def test_uploadedmedia_str(self):
        um = UploadedMedia.objects.get(pk=1)
        self.assertEqual(
            'uploaded/2020/11/sample_video.m4v',
            str(um))

    def test_media_filename(self):
        um = UploadedMedia.objects.get(pk=1)
        self.assertEqual('sample_video.m4v',
                         um.filename())

    def test_uploadedmedia_file_missing_new_delete(self):
        um = UploadedMedia.objects.create(create_user=self.admin_user,
                                          update_user=self.admin_user,
                                          file="my_media_file2.m4v")
        um.delete()
        self.assertRaises(OSError)
