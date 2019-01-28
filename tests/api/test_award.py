
# AwardsResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class AwardsResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json']

    def setUp(self):
        super(AwardsResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.auth_data = {
            'username': 'demo',
            'api_key': api_key.key,
        }
        self.url = get_api_url('awards')

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

    # check authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    # check returning a set of objects - expecting zero
    def test_no_objects(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
