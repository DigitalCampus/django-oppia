
import unittest
import pytest

from django.core.exceptions import MultipleObjectsReturned

from rest_framework.test import APITestCase

from oppia.models import Course, CourseStatus
from tests.utils import update_course_status
from tests.api.v3 import utils


class CourseAPITests(APITestCase):
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

    url = '/api/v3/course/'

    def setUp(self):
        super(CourseAPITests, self).setUp()
        utils.copy_test_courses(['anc_test_course.zip'])

    def perform_get_request(self, course_ref, headers):
        resource_url = self.url + str(course_ref) + "/"
        response = self.client.get(resource_url, headers=headers)
        return response

    # Put invalid
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_put_invalid(self):
        response = self.client.put(self.url, data={}, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # delete invalid
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_delete_invalid(self):
        response = self.client.delete(self.url, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # test unauthorized
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_unauthorized(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_invalid())
        self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

    # test contains courses (and right no of courses)
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_has_courses(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        # should have 4 courses with the test data set
        self.assertEqual(4, len(response_data))
        # check each course had a download url
        for course in response_data:
            self.assertTrue('resource_uri' in course)
            self.assertTrue('id' in course)
            self.assertTrue('version' in course)
            self.assertTrue('title' in course)
            self.assertTrue('description' in course)
            self.assertTrue('shortname' in course)
            self.assertTrue('priority' in course)
            self.assertTrue('status' in course)
            self.assertTrue('restricted' in course)
            self.assertTrue('url' in course)
            self.assertTrue('author' in course)
            self.assertTrue('username' in course)
            self.assertTrue('organisation' in course)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single(self):
        response = self.perform_get_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertTrue('resource_uri' in course)
        self.assertTrue('id' in course)
        self.assertTrue('version' in course)
        self.assertTrue('title' in course)
        self.assertTrue('description' in course)
        self.assertTrue('shortname' in course)
        self.assertTrue('priority' in course)
        self.assertTrue('status' in course)
        self.assertTrue('restricted' in course)
        self.assertTrue('url' in course)
        self.assertTrue('author' in course)
        self.assertTrue('username' in course)
        self.assertTrue('organisation' in course)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_not_found(self):
        response = self.perform_get_request(999, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_draft_nonvisible(self):
        response = self.perform_get_request(3, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_draft_admin_visible(self):
        response = self.perform_get_request(3, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 3)
        self.assertEqual(course['version'], 20150611100319)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_enabled_normal_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_get_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_enabled_staff_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_get_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_enabled_teacher_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_get_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_enabled_admin_visible(self):
        update_course_status(1, CourseStatus.LIVE)
        response = self.perform_get_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_disabled_normal_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_get_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_disabled_staff_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_get_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_disabled_teacher_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_get_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_new_downloads_disabled_admin_visible(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)
        response = self.perform_get_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_read_only_normal_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_get_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_read_only_staff_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_get_request(1, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_read_only_teacher_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_get_request(1, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_single_read_only_admin_visible(self):
        update_course_status(1, CourseStatus.READ_ONLY)
        response = self.perform_get_request(1, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertEqual(course['id'], 1)
        self.assertEqual(course['version'], 20150611095753)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_shortname_get_single(self):
        response = self.perform_get_request('anc1-all', utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertTrue('resource_uri' in course)
        self.assertTrue('id' in course)
        self.assertTrue('version' in course)
        self.assertTrue('title' in course)
        self.assertTrue('description' in course)
        self.assertTrue('shortname' in course)
        self.assertTrue('priority' in course)
        self.assertTrue('status' in course)
        self.assertTrue('restricted' in course)
        self.assertTrue('url' in course)
        self.assertTrue('author' in course)
        self.assertTrue('username' in course)
        self.assertTrue('organisation' in course)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_shortname_get_single_staff(self):
        response = self.perform_get_request('anc1-all', utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        course = response.json()
        self.assertTrue('resource_uri' in course)
        self.assertTrue('id' in course)
        self.assertTrue('version' in course)
        self.assertTrue('title' in course)
        self.assertTrue('description' in course)
        self.assertTrue('shortname' in course)
        self.assertTrue('priority' in course)
        self.assertTrue('status' in course)
        self.assertTrue('restricted' in course)
        self.assertTrue('url' in course)
        self.assertTrue('author' in course)
        self.assertTrue('username' in course)
        self.assertTrue('organisation' in course)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_shortname_get_single_not_found(self):
        response = self.perform_get_request('does-not-exist', utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_shortname_get_multiple_found(self):
        # add a temp course with same shortname as another
        course = Course()
        course.shortname = 'anc1-all'
        course.version = 123456789
        course.save()

        response = self.perform_get_request('anc1-all', utils.get_auth_header_user())
        self.assertRaises(MultipleObjectsReturned)
        self.assertEqual(response.status_code, 300)
