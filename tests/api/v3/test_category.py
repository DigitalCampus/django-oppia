import unittest
import pytest


from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from oppia.models import CourseStatus, CoursePermissions, Course, Cohort, CourseCohort, Participant, Category
from tests.utils import update_course_status

from tests.api.v3 import utils


class CategoryAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json']

    url = '/api/v3/category/'

    def assert_valid_response_and_get_tags(self, response):
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        category = response_data[0]
        self.assertTrue('count' in category)
        self.assertTrue('count_new_downloads_enabled' in category)
        self.assertTrue('course_statuses' in category)
        self.assertTrue('description' in category)
        self.assertTrue('highlight' in category)
        self.assertTrue('icon' in category)
        self.assertTrue('id' in category)
        self.assertTrue('name' in category)
        self.assertTrue('order_priority' in category)
        return response_data

    def assert_course_statuses(self, headers, expected):
        response = self.client.get(self.url, headers=headers)
        categories = self.assert_valid_response_and_get_tags(response)
        course_statuses = self.get_category_attr_in_results(categories, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def get_category_attr_in_results(self, tags, category, attr=None):
        return next((tag[attr] if attr else tag for tag in tags if tag['name'] == category))

    # check post not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_post_invalid(self):
        response = self.client.post(self.url, data={}, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # check delete not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_delete_invalid(self):
        response = self.client.delete(self.url, data={}, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # test unauthorized
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_unauthorized(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_invalid())
        self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

    # test authorized
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_authorized(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)

    # test valid json response and with 5 tags
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_has_categories(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())

        categories = self.assert_valid_response_and_get_tags(response)
        # should have 5 tags with the test data set
        self.assertEqual(5, len(categories))
        # check each course had a download url
        for category in categories:
            self.assertTrue('count' in category)
            self.assertTrue('id' in category)
            self.assertTrue('name' in category)
            # check count not 0
            self.assertTrue(category['count'] > 0)
            # check name not null
            self.assertTrue(len(category['name']) > 0)

    # test getting a listing of courses for one of the categories
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_category_list(self):
        response = self.client.get(self.url + "2/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        self.assertTrue('courses' in response_data)
        self.assertTrue('count' in response_data)
        self.assertTrue('name' in response_data)
        self.assertTrue('id' in response_data)
        self.assertEqual(len(response_data['courses']), response_data['count'])
        for course in response_data['courses']:
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

    # test getting listing of courses for an invalid tag
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_category_not_found(self):
        response = self.client.get(self.url + "999/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    # Expected count of courses having new downloads enabled by category (based on test_oppia.json)
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_count_new_downloads_enabled(self):

        expected = {'HEAT': 2, 'ANC': 1, 'Antenatal Care': 1, 'NCD': 1, 'reference': 0}

        # Disable new downloads from 1 of the 4 courses (ref-1)
        update_course_status(4, CourseStatus.NEW_DOWNLOADS_DISABLED)

        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        categories = self.assert_valid_response_and_get_tags(response)
        for category in categories:
            self.assertTrue('count_new_downloads_enabled' in category)
            self.assertEqual(category['count_new_downloads_enabled'], expected.get(category['name']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_statuses(self):
        # Expected courses having new downloads disabled by category (based on test_oppia.json)
        expected = {
            'HEAT': {'anc1-all': 'live', 'ncd1-et': 'new_downloads_disabled'},
            'ANC': {'anc1-all': 'live'},
            'Antenatal Care': {'anc1-all': 'live'},
            'NCD': {'ncd1-et': 'new_downloads_disabled'},
            'reference': {'ref-1': 'new_downloads_disabled'}
            }

        # Disable new downloads from 2 of the 4 courses (ncd1-et and ref-1)
        update_course_status(2, CourseStatus.NEW_DOWNLOADS_DISABLED)
        update_course_status(4, CourseStatus.NEW_DOWNLOADS_DISABLED)

        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        categories = self.assert_valid_response_and_get_tags(response)
        for category in categories:
            self.assertTrue('course_statuses' in category)
            self.assertEqual(expected.get(category['name']), category['course_statuses'])

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_not_included_in_course_statuses_normal_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        self.assert_course_statuses(utils.get_auth_header_user(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_not_included_in_course_statuses_teacher_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        self.assert_course_statuses(utils.get_auth_header_teacher(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_included_in_course_statuses_staff_user(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        self.assert_course_statuses(utils.get_auth_header_staff(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_included_in_course_statuses_admin_user(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        self.assert_course_statuses(utils.get_auth_header_admin(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_included_in_course_statuses_normal_user_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }
        user = User.objects.get(username='demo')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=user,
            role=CoursePermissions.VIEWER
        )

        self.assert_course_statuses(utils.get_auth_header_user(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_included_in_course_statuses_normal_user_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }
        user = User.objects.get(username='demo')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=user,
            role=CoursePermissions.MANAGER
        )

        self.assert_course_statuses(utils.get_auth_header_user(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_included_in_course_statuses_normal_teacher_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }
        teacher = User.objects.get(username='teacher')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=teacher,
            role=CoursePermissions.VIEWER
        )

        self.assert_course_statuses(utils.get_auth_header_teacher(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_is_included_in_course_statuses_normal_teacher_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }
        teacher = User.objects.get(username='teacher')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=teacher,
            role=CoursePermissions.MANAGER
        )

        self.assert_course_statuses(utils.get_auth_header_teacher(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_normal_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        self.assert_course_statuses(utils.get_auth_header_user(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_teacher_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        self.assert_course_statuses(utils.get_auth_header_teacher(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_staff_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        self.assert_course_statuses(utils.get_auth_header_staff(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_admin_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        self.assert_course_statuses(utils.get_auth_header_admin(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_normal_user_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)
        user = User.objects.get(username='demo')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=user,
            role=CoursePermissions.VIEWER
        )

        self.assert_course_statuses(utils.get_auth_header_user(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_normal_user_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        user = User.objects.get(username='demo')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=user,
            role=CoursePermissions.MANAGER
        )

        self.assert_course_statuses(utils.get_auth_header_user(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_teacher_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)
        teacher = User.objects.get(username='teacher')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=teacher,
            role=CoursePermissions.VIEWER
        )

        self.assert_course_statuses(utils.get_auth_header_teacher(), expected)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_archived_course_is_not_included_in_course_statuses_teacher_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)
        teacher = User.objects.get(username='teacher')
        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=teacher,
            role=CoursePermissions.MANAGER
        )

        self.assert_course_statuses(utils.get_auth_header_teacher(), expected)

    # Tests related with courses restricted to cohorts
    def setup_cohort(self):
        course1 = Course.objects.get(shortname='ref-1')
        course1.restricted = True
        course1.save()

        course2 = Course.objects.get(shortname='anc1-all')
        course2.restricted = True
        course2.save()

        cohort = Cohort.objects.create(description='Test')
        CourseCohort.objects.create(cohort=cohort, course=course1)
        CourseCohort.objects.create(cohort=cohort, course=course2)

        return cohort

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_admin_restricted_courses_in_category_list(self):
        self.setup_cohort()
        response = self.client.get(self.url, headers=utils.get_auth_header_admin())
        categories = self.assert_valid_response_and_get_tags(response)

        category_count = self.get_category_attr_in_results(categories, 'HEAT', 'count')
        self.assertEqual(len(categories), 5)
        self.assertEqual(category_count, 2)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_non_cohort_user_restricted_courses_in_category_list(self):
        self.setup_cohort()
        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        categories = self.assert_valid_response_and_get_tags(response)

        # There is a couple of categories (the ones related to ANC) that have all restricted courses
        # as well as the reference category (one restricted and one draft)
        category_count = self.get_category_attr_in_results(categories, 'HEAT', 'count')
        self.assertEqual(len(categories), 2)
        self.assertEqual(category_count, 1)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_cohort_user_restricted_courses_in_category_list(self):
        cohort = self.setup_cohort()
        user = User.objects.get(username='demo')
        Participant.objects.create(cohort=cohort, user=user, role=Participant.STUDENT)

        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        categories = self.assert_valid_response_and_get_tags(response)

        category_count = self.get_category_attr_in_results(categories, 'HEAT', 'count')
        self.assertEqual(len(categories), 5)
        self.assertEqual(category_count, 2)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_admin_restricted_courses_in_category_detail(self):
        self.setup_cohort()
        heat = Category.objects.get(name='HEAT')

        response = self.client.get(self.url + str(heat.pk) + "/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

        ref = Category.objects.get(name='reference')
        response = self.client.get(self.url + str(ref.pk) + "/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_cohort_user_restricted_courses_in_category_detail(self):
        cohort = self.setup_cohort()
        user = User.objects.get(username='demo')
        Participant.objects.create(cohort=cohort, user=user, role=Participant.STUDENT)

        heat = Category.objects.get(name='HEAT')
        response = self.client.get(self.url + str(heat.pk) + "/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

        ref = Category.objects.get(name='reference')
        response = self.client.get(self.url + str(ref.pk) + "/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_non_cohort_user_restricted_courses_in_category_detail(self):
        self.setup_cohort()

        heat = Category.objects.get(name='HEAT')
        response = self.client.get(self.url + str(heat.pk) + "/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)

        ref = Category.objects.get(name='reference')
        response = self.client.get(self.url + str(ref.pk) + "/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)
