import os
import shutil

from django.conf import settings
from django.urls import reverse
from oppia.models import Tracker, CourseStatus
from oppia.test import OppiaTestCase

from tests.utils import update_course_status


class DownloadViewTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_course_statuses.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']
    STR_EXPECTED_CONTENT_TYPE = 'application/zip'
    TEST_COURSES = ['anc_test_course.zip']

    def setUp(self):
        super(DownloadViewTest, self).setUp()
        self.course_download_url_valid = reverse('oppia:course_download',
                                                 args=[1])
        self.course_download_url_invalid = reverse('oppia:course_download',
                                                   args=[123])
        self.copy_test_courses()

    # Copy test courses to upload directory
    def copy_test_courses(self):
        for test_course in self.TEST_COURSES:
            src = os.path.join(settings.TEST_RESOURCES, test_course)
            dst = os.path.join(settings.COURSE_UPLOAD_DIR, test_course)
            shutil.copyfile(src, dst)

    def test_live_course_admin(self):
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    def test_live_course_staff(self):
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    def test_live_course_teacher(self):
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    def test_live_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_admin(self):
        update_course_status(1, CourseStatus.DRAFT)
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

    def test_draft_course_staff(self):
        update_course_status(1, CourseStatus.DRAFT)
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

    def test_draft_course_teacher(self):
        update_course_status(1, CourseStatus.DRAFT)
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_draft_course_normal(self):
        update_course_status(1, CourseStatus.DRAFT)
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_archived_course_admin(self):
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_archived_course_staff(self):
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_archived_course_teacher(self):
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_archived_course_normal(self):
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_new_downloads_disabled_course_admin(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

    def test_new_downloads_disabled_course_staff(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

    def test_new_downloads_disabled_course_teacher(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_new_downloads_disabled_course_normal(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 404)
        update_course_status(1, CourseStatus.LIVE)

    def test_read_only_course_admin(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.get_view(self.course_download_url_valid,
                                 self.admin_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

    def test_read_only_course_staff(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.get_view(self.course_download_url_valid,
                                 self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

    def test_read_only_course_teacher(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.get_view(self.course_download_url_valid,
                                 self.teacher_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

    def test_read_only_course_normal(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.get_view(self.course_download_url_valid,
                                 self.normal_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_status(1, CourseStatus.LIVE)

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
