import unittest
import pytest
import json

from rest_framework.test import APITestCase
from settings import constants
from settings.models import SettingProperties
from tests.api.v3 import utils


class UserRegisterTests(APITestCase):
    fixtures = ['tests/test_user.json']

    url = '/api/v3/user/'

    # check get method not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_get_list_invalid(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_admin())
        self.assertEqual(utils.HTTP_METHOD_NOT_ALLOWED, response.status_code)

    # check posting with no username
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_no_username(self):
        data = {
            'password': 'secret',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        self.assertEqual(msg['username'], ['This field is required.'])

    # check posting with no password
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_no_password(self):
        data = {
            'username': 'demo2',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        self.assertEqual(msg['password'], ['This field is required.'])

    # check posting with no email
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_no_email(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_CREATED, response.status_code)
        user_data = response.json()
        self.assertTrue('api_key' in user_data)
        self.assertTrue('email' in user_data)
        self.assertTrue('first_name' in user_data)
        self.assertTrue('last_name' in user_data)
        self.assertTrue('points' in user_data)
        self.assertTrue('username' in user_data)
        self.assertTrue('password' not in user_data)
        self.assertTrue('passwordagain' not in user_data)

    # check posting with invalid email
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_invalid_email(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'thisisnotanemailaddress',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['email'], ['Invalid email address format.'])

    # check posting with no passwordagain
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_no_passwordagain(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['passwordagain'], ['This field is required.'])

    # test no firstname
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_no_firstname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['first_name'], ['This field is required.'])

    # test firstname long enough
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_firstname_length(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'd',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['first_name'], ['Firstname not long enough'])

    # test no lastname
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_no_lastname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['last_name'], ['This field is required.'])

    # test password long enough
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_password_length(self):
        data = {
            'username': 'demo2',
            'password': 's',
            'passwordagain': 's',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['password'], ['password not long enough'])

    # test password and password again not matching
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_password_match(self):
        data = {
            'username': 'demo2',
            'password': 's',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['password'], ['passwords dont match'])

    # test lastname not long enough
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_lastname_length(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'u',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['last_name'], ['last_name not long enough'])

    # test created (all data valid)
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_post_created(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_CREATED, response.status_code)
        user_data = response.json()
        self.assertTrue('api_key' in user_data)
        self.assertTrue('email' in user_data)
        self.assertTrue('first_name' in user_data)
        self.assertTrue('last_name' in user_data)
        self.assertTrue('points' in user_data)
        self.assertTrue('username' in user_data)
        self.assertTrue('password' not in user_data)
        self.assertTrue('passwordagain' not in user_data)

    # test username already in use
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_username_in_use(self):
        data = {
            'username': 'demo',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['username'], ['A user with that username already exists.'])

    # test email address already in use
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_email_in_use(self):
        data = {
            'username': 'demo3',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@me.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['email'], ['email is already in use'])

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_self_registration_disabled_cant_view(self):
        # turn off self registration
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION, False)
        data = {
            'username': 'demo3',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo3@me.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        msg = response.json()
        # actual error message return may be different
        self.assertEqual(msg['message'], ['self registration is disabled'])

        # turn back on
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION, True)
