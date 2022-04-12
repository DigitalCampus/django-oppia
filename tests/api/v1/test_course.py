import os
import shutil

import pytest

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url, update_course_visibility
from oppia.models import Tracker


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
        user = User.objects.get(username='demo')
        admin = User.objects.get(username='admin')
        staff = User.objects.get(username='staff')
        teacher = User.objects.get(username='teacher')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=admin).key
        }
        self.staff_auth = {
            'username': 'staff',
            'api_key': get_api_key(user=staff).key
        }
        self.teacher_auth = {
            'username': 'teacher',
            'api_key': get_api_key(user=teacher).key
        }
        self.url = get_api_url('v1', 'course')

        self.copy_test_courses()

    # Copy test courses to upload directory
    def copy_test_courses(self):
        for test_course in self.TEST_COURSES:
            src = os.path.join(settings.TEST_RESOURCES, test_course)
            dst = os.path.join(settings.COURSE_UPLOAD_DIR, test_course)
            shutil.copyfile(src, dst)

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
        resource_url = get_api_url('v1', 'course', 1)
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
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
        resource_url = get_api_url('v1', 'course', 999)
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_get_single_draft_nonvisible(self):
        resource_url = get_api_url('v1', 'course', 3)
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_get_single_draft_admin_visible(self):
        resource_url = get_api_url('v1', 'course', 3)
        resp = self.api_client.get(
            resource_url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_download_file_zip_not_found(self):
        resource_url = get_api_url('v1', 'course', 5) + self.STR_DOWNLOAD
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_download_file_course_not_found(self):
        resource_url = get_api_url('v1', 'course', 999) + self.STR_DOWNLOAD
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_download_draft_nonvisible(self):
        resource_url = get_api_url('v1', 'course', 3) + self.STR_DOWNLOAD
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_get_activity(self):
        resource_url = get_api_url('v1', 'course', 1) + self.STR_ACTIVITY
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)

    def test_course_get_activity_notfound(self):
        resource_url = get_api_url('v1', 'course', 999) + self.STR_ACTIVITY
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_get_activity_draft_nonvisible(self):
        resource_url = get_api_url('v1', 'course', 3) + self.STR_ACTIVITY
        resp = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_course_get_activity_draft_admin_visible(self):
        resource_url = get_api_url('v1', 'course', 3) + self.STR_ACTIVITY
        resp = self.api_client.get(
            resource_url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)

    def test_live_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.teacher_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, True, False)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        update_course_visibility(1, False, False)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, True, False)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        update_course_visibility(1, False, False)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, True, False)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.teacher_auth)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, True, False)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, False, True)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.admin_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, False, True)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.staff_auth)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, False, True)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.teacher_auth)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_archived_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        update_course_visibility(1, False, True)
        resource_url = get_api_url('v1', 'course', 1) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    # Course does not exist
    def test_dne_course_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1123) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.admin_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_dne_course_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1123) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.staff_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_dne_course_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1123) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.teacher_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_dne_course_normal(self):
        tracker_count_start = Tracker.objects.all().count()
        resource_url = get_api_url('v1', 'course', 1123) + self.STR_DOWNLOAD
        response = self.api_client.get(
            resource_url, format='json', data=self.user_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)
