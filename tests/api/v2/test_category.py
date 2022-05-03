
# TODO TagResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import CourseStatus
from tests.utils import get_api_key, get_api_url, update_course_status


class CategoryResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json']

    def setUp(self):
        super(CategoryResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.auth_data = {
            'username': 'demo',
            'api_key': api_key.key,
        }
        self.url = get_api_url('v2', 'tag')

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
            self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)

    # test valid json response and with 5 tags
    def test_has_categories(self):
        resp = self.api_client.get(
            self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        # should have 5 tags with the test data set
        self.assertEqual(5, len(response_data['tags']))
        # check each course had a download url
        for tag in response_data['tags']:
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
                                   data=self.auth_data)
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
                                   data=self.auth_data)
        self.assertHttpNotFound(resp)

    def test_count_new_downloads_enabled(self):
        # Expected count of courses having new downloads enabled by category (based on test_oppia.json)
        expected = {'HEAT': 2, 'ANC': 1, 'Antenatal Care': 1, 'NCD': 1, 'reference': 1}

        # Disable new downloads from 1 of the 4 courses (ref-1)
        update_course_status(4, CourseStatus.NEW_DOWNLOADS_DISABLED)

        resp = self.api_client.get(
            self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        for tag in response_data['tags']:
            self.assertTrue('count_new_downloads_enabled' in tag)
            self.assertEqual(tag['count_new_downloads_enabled'], expected.get(tag['name']))

    def test_course_statuses(self):
        # Expected courses having new downloads disabled by category (based on test_oppia.json)
        expected = {
                    'HEAT':
                        {'anc1-all': 'live',
                         'ncd1-et': 'new_downloads_disabled'},
                    'ANC':
                        {'anc1-all': 'live'},
                    'Antenatal Care':
                        {'anc1-all': 'live'},
                    'NCD':
                        {'ncd1-et': 'new_downloads_disabled'},
                    'reference':
                        {'ref-1': 'new_downloads_disabled',
                         'draft-test': 'draft'}
                    }

        # Disable new downloads from 2 of the 4 courses (ncd1-et and ref-1)
        update_course_status(2, CourseStatus.NEW_DOWNLOADS_DISABLED)
        update_course_status(4, CourseStatus.NEW_DOWNLOADS_DISABLED)

        resp = self.api_client.get(
            self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        for tag in response_data['tags']:
            self.assertTrue('course_statuses' in tag)
            self.assertEqual(expected.get(tag['name']), tag['course_statuses'])
