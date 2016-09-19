# UserResource
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin


class UserResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['user.json', 'oppia.json']

    def setUp(self):
        super(UserResourceTest, self).setUp()
        self.url = '/api/v1/user/'

    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url, format='json'))

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
        self.assertTrue('api_key' in response_data)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        # check it doesn't contain the password
        self.assertFalse('password' in response_data)

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
