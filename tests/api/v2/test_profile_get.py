# UserResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class UserProfileTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_customfields.json']

    def setUp(self):
        super().setUp()
        self.url = get_api_url('v2', 'profile')

        user = User.objects.get(username='demo')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=user).key,
        }

    # check get not allowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json'))

    def test_get_invalid_apikey(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))

    def test_get_anonymous_user(self):
        resp = self.api_client.get(self.url, format='json')
        self.assertHttpUnauthorized(resp)

    def test_get_valid_user(self):
        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        self.assertValidJSON(resp.content)

        # check return data
        response_data = self.deserialize(resp)
        # check that cohorts and custom fields are included
        self.assertIn('country', response_data)
        self.assertIn('cohorts', response_data)
