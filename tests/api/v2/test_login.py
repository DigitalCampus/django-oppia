# UserResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class UserResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_customfields.json']

    def setUp(self):
        super(UserResourceTest, self).setUp()
        self.url = get_api_url('v2', 'user')
        user = User.objects.get(username='demo')
        self.valid_api_key = get_api_key(user=user)

    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url,
                                                            format='json'))

    # check valid login
    def test_valid_login(self):
        data = {
            'username': 'demo',
            'password': 'password'
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        # check return data
        response_data = self.deserialize(resp)

        # check that the api key exists and is the correct one
        self.assertTrue('api_key' in response_data)
        api_key = response_data['api_key']
        self.assertEqual(api_key, self.valid_api_key.key)

        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        self.assertTrue('email' in response_data)
        self.assertTrue('job_title' in response_data)
        self.assertTrue('organisation' in response_data)
        self.assertTrue('first_name' in response_data)
        self.assertTrue('last_name' in response_data)
        self.assertFalse('password' in response_data)  # check it doesn't contain the password
        self.assertTrue('cohorts' in response_data)
        self.assertTrue('badging' in response_data)
        self.assertTrue('scoring' in response_data)
        self.assertTrue('username' in response_data)
        self.assertTrue('metadata' in response_data)
        self.assertTrue('resource_uri' in response_data)

        self.assertEqual(100, response_data['points'])
        self.assertEqual(0, response_data['badges'])
        self.assertTrue(response_data['badging'])
        self.assertTrue(response_data['scoring'])
        self.assertEqual("demo@me.com", response_data['email'])
        self.assertEqual("", response_data['organisation'])
        self.assertEqual("", response_data['job_title'])
        self.assertEqual("demo", response_data['first_name'])
        self.assertEqual("user", response_data['last_name'])
        self.assertEqual("demo", response_data['username'])

    # check inactive user can't access
    def test_inactive_username(self):
        user = User.objects.get(username='demo')
        user.is_active = False
        user.save()

        data = {
            'username': 'demo',
            'password': 'password'
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data)

        # rest back to active
        user.is_active = True
        user.save()

    # check no username
    def test_no_username(self):
        data = {
            'password': 'demo'
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data)

    # check no password
    def test_no_password(self):
        data = {
            'username': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data)

    # check no username or password
    def test_no_username_password(self):
        data = {}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data)

    # check invalid password
    def test_invalid_password(self):
        data = {
            'username': 'user',
            'password': 'demo123'
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data)
