# PointsResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class PointsResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json']

    def setUp(self):
        super(PointsResourceTest, self).setUp()
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('points')

    # check get not allowed
    def test_get_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json'))

    # check post not allowed
    def test_post_not_allowed(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # check get with an invalid apiKey
    def test_get_apikeyinvalid(self):
        auth_header = self.create_apikey(username=self.username, api_key="badbadbad")
        self.assertHttpUnauthorized(
            self.api_client.get(self.url, forma='json', authentication=auth_header))

    # check a valid get
    def test_get_points(self):
        auth_header = self.create_apikey(username=self.username, api_key=self.api_key)
        res = self.api_client.get(self.url, format='json', authentication=auth_header)
        self.assertHttpOK(res)
        self.assertValidJSON(res.content)
