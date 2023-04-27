# UserResource
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class PasswordResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json']

    def setUp(self):
        super().setUp()
        self.url = get_api_url('v2', 'password')
        self.username = 'demo'
        self.user = User.objects.get(username=self.username)
        self.api_key = get_api_key(user=self.user).key

    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)

    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url, format='json'))

    # check valid password change
    def test_valid_change(self):

        old_login_data = {
            'username': 'demo',
            'password': 'password'
        }
        new_login_data = {
            'username': 'demo',
            'password': 'new_password'
        }
        password_change_data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        login_url = get_api_url('v2', 'user')

        login_attempt = self.api_client.post(login_url,
                                             format='json',
                                             data=old_login_data)
        self.assertHttpCreated(login_attempt)
        self.assertValidJSON(login_attempt.content)

        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=password_change_data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)

        # Check that the previous login fails
        login_attempt = self.api_client.post(login_url,
                                             format='json',
                                             data=old_login_data)
        self.assertHttpBadRequest(login_attempt)

        # Check that is the new one that is correct
        login_attempt = self.api_client.post(login_url,
                                             format='json',
                                             data=new_login_data)
        self.assertHttpCreated(login_attempt)

    # check inactive user can't access
    def test_no_password_repeat(self):

        data = {
            'new_password1': 'new_password'
        }
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('errors' in response_data)
        self.assertTrue('new_password2' in response_data['errors'])

    # check no username
    def test_no_matching_passwords(self):

        data = {
            'new_password1': 'new_password',
            'new_password2': 'different_password'
        }
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('errors' in response_data)
        self.assertTrue('new_password2' in response_data['errors'])
