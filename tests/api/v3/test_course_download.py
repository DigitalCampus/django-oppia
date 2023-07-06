import unittest
import pytest

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from oppia.models import Tracker, CourseStatus
from tests.utils import update_course_status, update_course_owner
from tests.api.v3 import utils


class CourseDownloadAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json',
                'tests/test_cohort.json',
                'tests/test_progress_summary.json',
                'tests/test_tracker.json']

    # @TODO confirm final endpoint for downloading course
    download_url = '/api/v3/course/download/'

    ZIP_EXPECTED_CONTENT_TYPE = 'application/zip'

    def setUp(self):
        super(CourseDownloadAPITests, self).setUp()
        utils.copy_test_courses(['anc_test_course.zip'])
        self.teacher = User.objects.get(username="teacher")

    def perform_download_request(self, course_ref, headers):
        resource_url = self.download_url + str(course_ref) + "/"
        response = self.client.get(resource_url, headers=headers)
        return response

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_download_file_zip_not_found(self):
        response = self.perform_download_request(5, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_download_file_course_not_found(self):
        response = self.perform_download_request(999, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_download_draft_nonvisible(self):
        response = self.perform_download_request(3, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_enabled_normal(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_enabled_teacher(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_enabled_staff(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_enabled_admin(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_disabled_normal(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_disabled_teacher(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_disabled_staff(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_new_downloads_disabled_admin(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_read_only_normal(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_read_only_teacher(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_read_only_staff(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_download_course_read_only_admin(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_teacher_owner(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        update_course_owner(1, self.teacher.id)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_new_downloads_disabled_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_new_downloads_disabled_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_new_downloads_disabled_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_new_downloads_disabled_course_teacher_owner(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        update_course_owner(1, self.teacher.id)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_new_downloads_disabled_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_read_only_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_read_only_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_read_only_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_read_only_course_teacher_owner(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        update_course_owner(1, self.teacher.id)
        response = self.perform_download_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_read_only_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_download_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    # Course does not exist
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_dne_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1123, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_dne_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1123, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_dne_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1123, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_dne_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request(1123, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_shortname_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request('anc1-all', utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_dne_course_shortname_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_download_request('does-not-exist', utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)
