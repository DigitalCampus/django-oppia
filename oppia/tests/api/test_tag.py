
# TODO TagResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.tests.utils import get_api_key, get_api_url


class TagResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['user.json', 'oppia.json']

    def setUp(self):
        super(TagResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.auth_data = {
            'username': 'demo',
            'api_key': api_key.key,
        }
        self.url = get_api_url('tag')

    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))

    # test authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)

    # test valid json response and with 5 tags
    def test_has_tags(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        # should have 5 tags with the test data set
        self.assertEquals(len(response_data['tags']), 4)
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
    def test_tag_list(self):
        resource_url = get_api_url('tag', 2)
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertTrue('count' in response_data)
        self.assertTrue('name' in response_data)
        self.assertEqual(len(response_data['courses']), response_data['count'])
        for course in response_data['courses']:
            self.assertTrue('shortname' in course)
            self.assertTrue('title' in course)
            self.assertTrue('url' in course)
            self.assertTrue('version' in course)

    # test getting listing of courses for an invalid tag
    def test_tag_not_found(self):
        resource_url = get_api_url('tag', 999)
        resp = self.api_client.get(resource_url, format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)

    #TODO check tags and permissions - so only tags that have course the user is allowed to view will appear
