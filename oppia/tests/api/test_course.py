# CourseResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.tests.utils import get_api_key, get_api_url


class CourseResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['user.json', 'oppia.json', 'permissions.json']

    def setUp(self):
        super(CourseResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        admin = User.objects.get(username='admin')
        self.auth_data = {
            'username': 'demo',
            'api_key': get_api_key(user=user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=admin).key
        }
        self.url = get_api_url('course')

    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'demo',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))

    # test authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)

    # test contains courses (and right no of courses)
    def test_has_courses(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        # should have 2 courses with the test data set
        self.assertEquals(len(response_data['courses']), 2)
        # check each course had a download url
        for course in response_data['courses']:
            self.assertTrue('url' in course)
            self.assertTrue('shortname' in course)
            self.assertTrue('title' in course)
            self.assertTrue('version' in course)

    def test_course_get_single(self):
        resource_url = get_api_url('course', 1)
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        # check course format
        course = self.deserialize(resp)
        self.assertTrue('shortname' in course)
        self.assertTrue('title' in course)
        self.assertTrue('description' in course)
        self.assertTrue('version' in course)

    def test_course_get_single_not_found(self):
        resource_url = get_api_url('course', 999)
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_course_get_single_draft_nonvisible(self):
        resource_url = get_api_url('course', 3)
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_course_get_single_draft_admin_visible(self):
        resource_url = get_api_url('course', 3)
        resp = self.api_client.get(resource_url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_course_download_file_zip_not_found(self):
        resource_url = get_api_url('course', 2) + 'download/'
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_course_download_file_course_not_found(self):
        resource_url = get_api_url('course', 999) + 'download/'
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_course_download_draft_nonvisible(self):
        resource_url = get_api_url('course', 3) + 'download/'
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_course_get_activity(self):
        resource_url = get_api_url('course', 1) + 'activity/'
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)

    def test_course_get_activity_notfound(self):
        resource_url = get_api_url('course', 999) + 'activity/'
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_course_get_activity_draft_nonvisible(self):
        resource_url = get_api_url('course', 3) + 'activity/'
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_course_get_acitivity_draft_admin_visible(self):
        resource_url = get_api_url('course', 3) + 'activity/'
        resp = self.api_client.get(resource_url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
