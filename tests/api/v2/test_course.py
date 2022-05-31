import os
import shutil

from django.conf import settings

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, \
    get_api_url, \
    update_course_status, \
    update_course_owner
from oppia.models import Tracker, Course, CourseStatus


class CourseResourceTest(ResourceTestCaseMixin, TransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json']

    STR_DOWNLOAD = 'download/'
    STR_ACTIVITY = 'activity/'
    STR_ZIP_EXPECTED_CONTENT_TYPE = 'application/zip'
    TEST_COURSES = ['anc_test_course.zip']

    def setUp(self):
        super(CourseResourceTest, self).setUp()
        self.user = User.objects.get(username='demo')
        self.admin = User.objects.get(username='admin')
        self.staff = User.objects.get(username='staff')
        self.teacher = User.objects.get(username='teacher')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=self.user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=self.admin).key
        }
        self.staff_auth = {
            'username': 'staff',
            'api_key': get_api_key(user=self.staff).key
        }
        self.teacher_auth = {
            'username': 'teacher',
            'api_key': get_api_key(user=self.teacher).key
        }
        self.url = get_api_url('v2', 'course')
        self.copy_test_courses()

    # Copy test courses to upload directory
    def copy_test_courses(self):
        for test_course in self.TEST_COURSES:
            src = os.path.join(settings.TEST_RESOURCES, test_course)
            dst = os.path.join(settings.COURSE_UPLOAD_DIR, test_course)
            shutil.copyfile(src, dst)

    def perform_request(self, course_id, user, path=''):
        resource_url = get_api_url('v2', 'course', course_id) + path
        resp = self.api_client.get(
            resource_url, format='json', data=user)
        return resp

    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.post(self.url, format='json', data={}))

    # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'demo',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(
            self.api_client.get(self.url, format='json', data=data))

    # test authorized
    def test_authorized(self):
        resp = self.api_client.get(
            self.url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)

    # test contains courses (and right no of courses)
    def test_has_courses(self):
        resp = self.api_client.get(
            self.url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        # should have 2 courses with the test data set
        self.assertEqual(3, len(response_data['courses']))
        # check each course had a download url
        for course in response_data['courses']:
            self.assertTrue('url' in course)
            self.assertTrue('shortname' in course)
            self.assertTrue('title' in course)
            self.assertTrue('version' in course)
            self.assertTrue('author' in course)
            self.assertTrue('organisation' in course)

    def test_course_get_single(self):
        resp = self.perform_request(1, self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        # check course format
        course = self.deserialize(resp)
        self.assertTrue('shortname' in course)
        self.assertTrue('title' in course)
        self.assertTrue('description' in course)
        self.assertTrue('version' in course)
        self.assertTrue('author' in course)
        self.assertTrue('organisation' in course)

    def test_course_get_single_not_found(self):
        resp = self.perform_request(999, self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_get_single_draft_nonvisible(self):
        resp = self.perform_request(3, self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_get_single_draft_admin_visible(self):
        resp = self.perform_request(3, self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_enabled_normal_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_enabled_staff_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.staff_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_enabled_teacher_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_enabled_admin_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_disabled_normal_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_disabled_staff_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.staff_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_disabled_teacher_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_new_downloads_disabled_admin_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_read_only_normal_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_read_only_staff_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.staff_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_read_only_teacher_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_get_single_read_only_admin_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_download_file_zip_not_found(self):
        resp = self.perform_request(5, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpNotFound(resp)

    def test_course_download_file_course_not_found(self):
        resp = self.perform_request(999, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpNotFound(resp)

    def test_course_download_draft_nonvisible(self):
        resp = self.perform_request(3, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpNotFound(resp)

    def test_download_course_new_downloads_enabled_normal(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_new_downloads_enabled_teacher(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_new_downloads_enabled_staff(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_new_downloads_enabled_admin(self):
        update_course_status(1, CourseStatus.LIVE)
        resp = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_new_downloads_disabled_normal(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_new_downloads_disabled_teacher(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_new_downloads_disabled_staff(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_new_downloads_disabled_admin(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        resp = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_read_only_normal(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_read_only_teacher(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_read_only_staff(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_download_course_read_only_admin(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        resp = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(resp)

    def test_course_get_activity(self):
        resp = self.perform_request(1, self.user_auth, self.STR_ACTIVITY)
        self.assertHttpOK(resp)

    def test_course_get_activity_notfound(self):
        resp = self.perform_request(999, self.user_auth, self.STR_ACTIVITY)
        self.assertHttpNotFound(resp)

    def test_course_get_activity_draft_nonvisible(self):
        resp = self.perform_request(3, self.user_auth, self.STR_ACTIVITY)
        self.assertHttpNotFound(resp)

    def test_course_get_activity_draft_admin_visible(self):
        resp = self.perform_request(3, self.admin_auth, self.STR_ACTIVITY)
        self.assertHttpOK(resp)

    def test_live_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_live_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_live_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_live_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_teacher_owner(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        update_course_owner(1, self.teacher.id)
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.DRAFT)
        response = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.ARCHIVED)
        response = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_new_downloads_disabled_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_new_downloads_disabled_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_new_downloads_disabled_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_new_downloads_disabled_course_teacher_owner(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        update_course_owner(1, self.teacher.id)
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_new_downloads_disabled_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_read_only_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_request(1, self.admin_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_read_only_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_request(1, self.staff_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_read_only_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_read_only_course_teacher_owner(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        update_course_owner(1, self.teacher.id)
        response = self.perform_request(1, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_read_only_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_request(1, self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    # Course does not exist
    def test_dne_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1123, self.admin_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_dne_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1123, self.staff_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_dne_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1123, self.teacher_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_dne_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request(1123, self.user_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_live_course_shortname_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request('anc1-all', self.user_auth, self.STR_DOWNLOAD)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_dne_course_shortname_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.perform_request('does-not-exist', self.user_auth, self.STR_DOWNLOAD)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_course_shortname_get_single(self):
        resp = self.perform_request('anc1-all', self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        # check course format
        course = self.deserialize(resp)
        self.assertTrue('shortname' in course)
        self.assertTrue('title' in course)
        self.assertTrue('description' in course)
        self.assertTrue('version' in course)
        self.assertTrue('author' in course)
        self.assertTrue('organisation' in course)

    def test_course_shortname_get_single_staff(self):
        resp = self.perform_request('anc1-all', self.staff_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        # check course format
        course = self.deserialize(resp)
        self.assertTrue('shortname' in course)
        self.assertTrue('title' in course)
        self.assertTrue('description' in course)
        self.assertTrue('version' in course)
        self.assertTrue('author' in course)
        self.assertTrue('organisation' in course)

    def test_course_shortname_get_single_not_found(self):
        resp = self.perform_request('does-not-exist', self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_shortname_get_multiple_found(self):
        # add a temp course with same shortname as another
        course = Course()
        course.shortname = 'anc1-all'
        course.version = 123456789
        course.save()

        resp = self.perform_request('anc1-all', self.user_auth)
        self.assertRaises(MultipleObjectsReturned)
        self.assertEqual(300, resp.status_code)
