import unittest
import pytest

from rest_framework.test import APITestCase
from tests.api.v3 import utils


class UserChangePasswordTests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json']

    url = '/api/v3/user/'
    login_url = '/api/v3/user/demo/'

    # check valid password change
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
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

        response = self.client.put(self.url, data=password_change_data, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)

        # Check that the previous login fails
        login_attempt = self.client.post(self.login_url, data=old_login_data)
        self.assertEqual(utils.HTTP_BAD_REQUEST, login_attempt.status_code)

        # Check that is the new one that is correct
        login_attempt = self.client.post(self.login_url, data=new_login_data)
        self.assertEqual(utils.HTTP_OK, login_attempt.status_code)

    # check inactive user can't access
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_no_password_repeat(self):

        data = {
            'new_password1': 'new_password'
        }
        response = self.client.post(self.url, data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        self.assertEqual(msg['errors'], ['new_password2'])

    # check no username
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_not_matching_passwords(self):

        data = {
            'new_password1': 'new_password',
            'new_password2': 'different_password'
        }
        response = self.client.post(self.url, data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        self.assertEqual(msg['errors'], ['new_password2'])
