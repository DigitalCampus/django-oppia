import os
import shutil

from django.conf import settings
from django.urls import reverse

from oppia.test import OppiaTestCase


class DownloadMediaTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_course_statuses.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json',
                'tests/test_av_uploadedmedia.json']

    STR_EXPECTED_CONTENT_TYPE = 'application/zip'
    UPLOADED_ROOT = os.path.join(settings.MEDIA_ROOT, 'uploaded', '2020', '11')
    MEDIA_FILENAME = 'sample_video.m4v'

    def setUp(self):
        super(DownloadMediaTest, self).setUp()
        os.makedirs(self.UPLOADED_ROOT, exist_ok=True)

    def test_permissions(self):
        url = reverse('av:course_media', args=[1])
        allowed_users = [self.admin_user,
                         self.staff_user,
                         self.teacher_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(url)
            self.assertTemplateUsed(response, 'course/media/list.html')
            self.assertEqual(200, response.status_code)

    def test_course_with_media(self):
        # copy sample video to correct location
        src = os.path.join(settings.TEST_RESOURCES, self.MEDIA_FILENAME)
        dst = os.path.join(self.UPLOADED_ROOT, self.MEDIA_FILENAME)
        shutil.copyfile(src, dst)

        self.client.force_login(self.normal_user)
        url = reverse('av:download_course_media', args=[1])
        response = self.client.get(url)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    def test_course_no_media(self):
        self.client.force_login(self.normal_user)
        url = reverse('av:download_course_media', args=[2])
        response = self.client.get(url)
        self.assertRedirects(response,
                             reverse('av:course_media',
                                     args=[2]) + "?error=no_media",
                             302,
                             200)

    def test_invalid_course(self):
        self.client.force_login(self.normal_user)
        url = reverse('av:download_course_media', args=[0])
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
