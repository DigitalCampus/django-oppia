# PointsResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.tests.utils import getApiKey


class PointsResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['user.json', 'oppia.json']

    def setUp(self):
        super(PointsResourceTest, self).setUp()
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = getApiKey(user=user)
        self.api_key = api_key.key
        self.url = '/api/v1/points/'

    # check get not allowed
    def test_get_not_found(self):
        self.assertHttpNotFound(self.api_client.get(self.url, format='json'))

    # check post not allowed
    def test_post_not_found(self):
        self.assertHttpNotFound(self.api_client.post(self.url, format='json', data={}))