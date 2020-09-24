import pytest

from django.forms import ValidationError
from django.urls import reverse
from oppia.test import OppiaTestCase


class ContentViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(ContentViewsTest, self).setUp()
        self.media_embed_helper_url = reverse('content:media_embed_helper')
        self.video_embed_helper_url = reverse('content:video_embed_helper')
        self.video_file_path = \
            './oppia/fixtures/reference_files/sample_video.m4v'

    # GET media embed helper
    def test_media_embed_helper_get_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(200, response.status_code)

    def test_media_embed_helper_get_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(200, response.status_code)

    def test_media_embed_helper_get_teacher(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(200, response.status_code)

    def test_media_embed_helper_get_normal(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(200, response.status_code)

    def test_media_embed_helper_get_anon(self):
        self.client.logout()
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(200, response.status_code)

    # POST media embed helper
    def test_media_embed_helper_post_empty_url(self):
        self.client.force_login(self.admin_user)
        media_url = ""
        response = self.client.post(self.media_embed_helper_url,
                                    {'media_url': media_url})
        self.assertRaises(ValidationError)
        self.assertEqual(200, response.status_code)

    def test_media_embed_helper_post_no_url(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.media_embed_helper_url, {})
        self.assertRaises(ValidationError)
        self.assertEqual(200, response.status_code)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_media_embed_helper_post_valid_url(self):
        self.client.force_login(self.admin_user)
        media_url = "https://downloads.digital-campus.org/media/anc/" \
            "iheed-20140217-breastfeeding-technique-part1.m4v"
        response = self.client.post(self.media_embed_helper_url,
                                    {'media_url': media_url})
        self.assertEqual(200, response.status_code)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_media_embed_helper_post_invalid_url(self):
        self.client.force_login(self.admin_user)
        media_url = "https://downloads.d/media/part1.m4v"
        response = self.client.post(self.media_embed_helper_url,
                                    {'media_url': media_url})
        self.assertRaises(IOError)
        self.assertEqual(200, response.status_code)
