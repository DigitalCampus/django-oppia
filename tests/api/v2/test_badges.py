from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class BadgesResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_badges.json']

    def setUp(self):
        super(BadgesResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.auth_data = {
            'username': 'demo',
            'api_key': api_key.key,
        }
        self.url = get_api_url('v2', 'badges')

    # check post not allowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # check unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'demo',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))

    # check correct
    def test_correct(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

        # check that the response contains 1 badge
        response_data = self.deserialize(resp)
        self.assertTrue('objects' in response_data)
        self.assertEqual(len(response_data['objects']), 1)
        badge = response_data['objects'][0]
        self.assertTrue('allow_multiple_awards' in badge)
        self.assertTrue('default_icon' in badge)
        self.assertTrue('description' in badge)
        self.assertTrue('id' in badge)
        self.assertTrue('name' in badge)
        self.assertTrue('points' in badge)
        self.assertTrue('ref' in badge)
