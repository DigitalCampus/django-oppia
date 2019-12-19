import pytest

from django.urls import reverse
from oppia.test import OppiaTestCase

from tests.utils import update_course_visibility


class DownloadViewTest(OppiaTestCase):

    STR_EXPECTED_CONTENT_TYPE = 'application/zip'

    def setUp(self):
        super(DownloadViewTest, self).setUp()
        self.course_download_url_valid = reverse('oppia_course_download',
                                                 args=[1])
        self.course_download_url_invalid = reverse('oppia_course_download',
                                                   args=[123])
        
    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_admin(self):
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_staff(self):
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_teacher(self):
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_normal(self):
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_draft_course_admin(self):
        update_course_visibility(1, True, False)
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_visibility(1, False, False)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_draft_course_staff(self):
        update_course_visibility(1, True, False)
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_visibility(1, False, False)

    def test_draft_course_teacher(self):
        update_course_visibility(1, True, False)
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_draft_course_normal(self):
        update_course_visibility(1, True, False)
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_admin(self):
        update_course_visibility(1, False, True)
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_staff(self):
        update_course_visibility(1, False, True)
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_teacher(self):
        update_course_visibility(1, False, True)
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_normal(self):
        update_course_visibility(1, False, True)
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    # Course does not exist
    def test_dne_course_admin(self):
        response = self.get_view(self.course_download_url_invalid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 404)

    def test_dne_course_staff(self):
        response = self.get_view(self.course_download_url_invalid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 404)

    def test_dne_course_teacher(self):
        response = self.get_view(self.course_download_url_invalid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 404)

    def test_dne_course_normal(self):
        response = self.get_view(self.course_download_url_invalid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 404)
