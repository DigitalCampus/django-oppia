
from oppia.test import OppiaTestCase
from av.models import UploadedMedia, UploadedMediaImage, image_file_name


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

    def test_uploadedmediaimage_str(self):
        um = UploadedMediaImage.objects.get(pk=1)
        self.assertEqual(
            'uploaded/images/fr/am/frame-001_71mRFnT.png',
            str(um))

    def test_media_filename(self):
        um = UploadedMedia.objects.get(pk=1)
        self.assertEqual('sample_video.m4v',
                         um.filename())

    def test_media_default_image_set(self):
        um = UploadedMedia.objects.get(pk=1)
        self.assertEqual('uploaded/images/fr/am/frame-001_71mRFnT.png',
                         um.get_default_image().image.name)

    def test_media_default_image_not_set(self):
        um = UploadedMedia.objects.get(pk=2)
        self.assertEqual('uploaded/images/fr/am/frame-004_DjG9Zk4.png',
                         um.get_default_image().image.name)

    def test_media_default_image_none(self):
        um = UploadedMedia.objects.get(pk=3)
        self.assertRaises(UploadedMediaImage.DoesNotExist)
        self.assertEqual(None, um.get_default_image())

    def test_uploadedmedia_file_missing_embed(self):
        um = UploadedMedia.objects.create(create_user=self.admin_user,
                                          update_user=self.admin_user,
                                          file="my_media_file.m4v")
        um.get_embed_code("http://mydomain.com/")
        self.assertRaises(FileNotFoundError)

    def test_uploadedmedia_file_missing_new_delete(self):
        um = UploadedMedia.objects.create(create_user=self.admin_user,
                                          update_user=self.admin_user,
                                          file="my_media_file2.m4v")
        um.delete()
        self.assertRaises(OSError)

    def test_uploadedmedia_image_filename(self):
        um = UploadedMedia.objects.get(pk=1)
        umi = UploadedMediaImage.objects.create(create_user=self.admin_user,
                                                image="my_media_file3.m4v",
                                                uploaded_media=um)
        name = image_file_name(umi, "my_media_file2.m4v")
        self.assertEqual("uploaded/images/my/_m/my_media_file2.m4v", name)

    def test_uploadedmedia_file_missing_existing_delete(self):
        um = UploadedMedia.objects.get(pk=1)
        umi = UploadedMediaImage.objects.create(create_user=self.admin_user,
                                                image="my_media_file3.m4v",
                                                uploaded_media=um)
        umi.delete()
        self.assertRaises(OSError)
