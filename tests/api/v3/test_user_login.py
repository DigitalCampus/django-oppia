import unittest
import pytest
import json

from rest_framework.test import APITestCase

from tests.api.v3 import utils


class UserLoginTests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_customfields.json']

    url = "/api/v3/login/"

    # check get not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_get_invalid(self):
        response = self.client.get(self.url)
        self.assertEqual(utils.HTTP_METHOD_NOT_ALLOWED, response.status_code)

    # check valid login
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_valid_login(self):
        data = {
            'username': 'demo',
            'password': 'password'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_OK, response.status_code)

        # check return data
        response_data = response.json()

        # check that the api key exists and is the correct one
        self.assertTrue('api_key' in response_data)
        api_key = response_data['api_key']
        self.assertEqual(api_key, "4512ef97bdc332db36c70127e374d181")

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
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_inactive_username(self):
        user = utils.get_normal_user()
        user.is_active = False
        user.save()

        data = {
            'username': 'demo',
            'password': 'password'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_UNAUTHORIZED, response.status_code)
        response_data = response.json()
        self.assertTrue('error' in response_data)

        # rest back to active
        user.is_active = True
        user.save()

    # check no username
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_no_username(self):
        data = {
            'password': 'demo'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        response_data = response.json()
        self.assertTrue('error' in response_data)

    # check no password
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_no_password(self):
        data = {
            'username': 'user',
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        response_data = response.json()
        self.assertTrue('error' in response_data)

    # check no username or password
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_no_username_password(self):
        data = {}
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
        response_data = response.json()
        self.assertTrue('error' in response_data)

    # check invalid password
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_invalid_password(self):
        data = {
            'username': 'user',
            'password': 'demo123'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(utils.HTTP_UNAUTHORIZED, response.status_code)
        response_data = response.json()
        self.assertTrue('error' in response_data)
