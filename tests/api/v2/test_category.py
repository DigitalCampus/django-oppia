
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import CourseStatus, CoursePermissions, Course, Cohort, CourseCohort, Participant, Category
from tests.utils import get_api_key, get_api_url, update_course_status


class CategoryResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json']

    def setUp(self):
        super(CategoryResourceTest, self).setUp()
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

        self.url = get_api_url('v2', 'tag')

    def assert_valid_response_and_get_tags(self, resp):
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        return response_data['tags']

    def get_category_attr_in_results(self, tags, category, attr=None):
        return next((tag[attr] if attr else tag for tag in tags if tag['name'] == category))

    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.post(self.url, format='json', data={}))

    # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(
            self.api_client.get(self.url, format='json', data=data))

    # test authorized
    def test_authorized(self):
        resp = self.api_client.get(
            self.url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)

    # test valid json response and with 5 tags
    def test_has_categories(self):
        resp = self.api_client.get(
            self.url, format='json', data=self.user_auth)

        tags = self.assert_valid_response_and_get_tags(resp)
        # should have 5 tags with the test data set
        self.assertEqual(5, len(tags))
        # check each course had a download url
        for tag in tags:
            self.assertTrue('count' in tag)
            self.assertTrue('id' in tag)
            self.assertTrue('name' in tag)
            # check count not 0
            self.assertTrue(tag['count'] > 0)
            # check name not null
            self.assertTrue(len(tag['name']) > 0)

    # test getting a listing of courses for one of the tags
    def test_category_list(self):
        resource_url = get_api_url('v2', 'tag', 2)
        resp = self.api_client.get(resource_url,
                                   format='json',
                                   data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertTrue('count' in response_data)
        self.assertTrue('name' in response_data)
        self.assertEqual(len(response_data['courses']),
                         response_data['count'])
        for course in response_data['courses']:
            self.assertTrue('shortname' in course)
            self.assertTrue('title' in course)
            self.assertTrue('url' in course)
            self.assertTrue('version' in course)

    # test getting listing of courses for an invalid tag
    def test_category_not_found(self):
        resource_url = get_api_url('v2', 'tag', 999)
        resp = self.api_client.get(resource_url,
                                   format='json',
                                   data=self.user_auth)
        self.assertHttpNotFound(resp)

    def test_count_new_downloads_enabled(self):
        # Expected count of courses having new downloads enabled by category (based on test_oppia.json)
        expected = {'HEAT': 2, 'ANC': 1, 'Antenatal Care': 1, 'NCD': 1, 'reference': 0}

        # Disable new downloads from 1 of the 4 courses (ref-1)
        update_course_status(4, CourseStatus.NEW_DOWNLOADS_DISABLED)

        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        for tag in tags:
            self.assertTrue('count_new_downloads_enabled' in tag)
            self.assertEqual(tag['count_new_downloads_enabled'], expected.get(tag['name']))

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

        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        for tag in tags:
            self.assertTrue('course_statuses' in tag)
            self.assertEqual(expected.get(tag['name']), tag['course_statuses'])

    def test_draft_course_is_not_included_in_course_statuses_normal_user(self):
        expected1 = {
            'reference': {'ref-1': 'live'}
        }

        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected1.get('reference'), course_statuses)

    def test_draft_course_is_not_included_in_course_statuses_teacher_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        resp = self.api_client.get(self.url, format='json', data=self.teacher_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_draft_course_is_included_in_course_statuses_staff_user(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        resp = self.api_client.get(self.url, format='json', data=self.staff_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_draft_course_is_included_in_course_statuses_admin_user(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_draft_course_is_included_in_course_statuses_normal_user_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.user,
            role=CoursePermissions.VIEWER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_draft_course_is_included_in_course_statuses_normal_user_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.user,
            role=CoursePermissions.MANAGER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_draft_course_is_included_in_course_statuses_normal_teacher_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.teacher,
            role=CoursePermissions.VIEWER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_draft_course_is_included_in_course_statuses_normal_teacher_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live', 'draft-test': 'draft'}
        }

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.teacher,
            role=CoursePermissions.MANAGER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_normal_user(self):
        expected1 = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected1.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_teacher_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        resp = self.api_client.get(self.url, format='json', data=self.teacher_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_staff_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        resp = self.api_client.get(self.url, format='json', data=self.staff_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_admin_user(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_normal_user_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.user,
            role=CoursePermissions.VIEWER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = next((tag['course_statuses'] for tag in tags if tag['name'] == 'reference'))
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_normal_user_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.user,
            role=CoursePermissions.MANAGER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = next((tag['course_statuses'] for tag in tags if tag['name'] == 'reference'))
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_normal_teacher_with_viewer_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.teacher,
            role=CoursePermissions.VIEWER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)

    def test_archived_course_is_not_included_in_course_statuses_normal_teacher_with_manager_permissions(self):
        expected = {
            'reference': {'ref-1': 'live'}
        }

        # Set draft-test course to archived status
        update_course_status(3, CourseStatus.ARCHIVED)

        # Add Viewer permission to normal user
        CoursePermissions.objects.create(
            course=Course.objects.get(shortname='draft-test'),
            user=self.teacher,
            role=CoursePermissions.MANAGER
        )

        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)
        course_statuses = self.get_category_attr_in_results(tags, 'reference', 'course_statuses')
        self.assertEqual(expected.get('reference'), course_statuses)


    ### Tests related with courses restricted to cohorts

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


    def test_admin_restricted_courses_in_category_list(self):
        self.setup_cohort()
        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        tags = self.assert_valid_response_and_get_tags(resp)

        category_count = self.get_category_attr_in_results(tags, 'HEAT', 'count')
        self.assertEqual(len(tags), 5)
        self.assertEqual(category_count, 2)


    def test_non_cohort_user_restricted_courses_in_category_list(self):
        self.setup_cohort()
        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        tags = self.assert_valid_response_and_get_tags(resp)

        # There is a couple of categories (the ones related to ANC) that have all restricted courses
        # as well as the reference category (one restricted and one draft)
        category_count = self.get_category_attr_in_results(tags, 'HEAT', 'count')
        self.assertEqual(len(tags), 2)
        self.assertEqual(category_count, 1)

    def test_cohort_user_restricted_courses_in_category_list(self):
        cohort = self.setup_cohort()
        Participant.objects.create(cohort=cohort, user=self.user, role=Participant.STUDENT)

        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        tags = self.assert_valid_response_and_get_tags(resp)

        category_count = self.get_category_attr_in_results(tags, 'HEAT', 'count')
        self.assertEqual(len(tags), 5)
        self.assertEqual(category_count, 2)


    def test_admin_restricted_courses_in_category_detail(self):
        self.setup_cohort()
        heat = Category.objects.get(name='HEAT')
        url = get_api_url('v2', 'tag', resource_id=heat.pk)

        resp = self.api_client.get(url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['courses']), 2)

        ref = Category.objects.get(name='reference')
        url = get_api_url('v2', 'tag', resource_id=ref.pk)
        resp = self.api_client.get(url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['courses']), 2)


    def test_cohort_user_restricted_courses_in_category_detail(self):

        cohort = self.setup_cohort()
        Participant.objects.create(cohort=cohort, user=self.user, role=Participant.STUDENT)
        heat = Category.objects.get(name='HEAT')
        url = get_api_url('v2', 'tag', resource_id=heat.pk)

        resp = self.api_client.get(url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['courses']), 2)

        ref = Category.objects.get(name='reference')
        url = get_api_url('v2', 'tag', resource_id=ref.pk)
        resp = self.api_client.get(url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['courses']), 1)


    def test_non_cohort_user_restricted_courses_in_category_detail(self):
        self.setup_cohort()
        heat = Category.objects.get(name='HEAT')
        url = get_api_url('v2', 'tag', resource_id=heat.pk)

        resp = self.api_client.get(url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['courses']), 1)

        ref = Category.objects.get(name='reference')
        url = get_api_url('v2', 'tag', resource_id=ref.pk)
        resp = self.api_client.get(url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertEqual(len(response_data['courses']), 0)


