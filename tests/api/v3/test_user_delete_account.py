import unittest
import pytest

from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from tests.api.v3 import utils


class DeleteAccountAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json']

    url = '/api/v3/user/'

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_get_list_invalid(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_METHOD_NOT_ALLOWED, response.status_code)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_get_individual_invalid(self):
        response = self.client.get(self.url + "3/", headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_METHOD_NOT_ALLOWED, response.status_code)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_deleted_own(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'password',
        }
        response = self.client.delete(self.url + "2/", data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_OK, response.status_code)
        response_data = response.json()
        self.assertTrue('message' in response_data)
        self.assertFalse('password' in response_data)

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start - 1, user_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_cannot_delete_others_account(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'password',
        }
        # normal user can't delete admin
        response = self.client.delete(self.url + "1/", data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_UNAUTHORIZED, response.status_code)

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)

    # invalid password
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_invalid_password(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'invalid',
        }
        response = self.client.delete(self.url + "2/", data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_UNAUTHORIZED, response.status_code)

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)

    # no password
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_no_password(self):
        user_count_start = User.objects.all().count()
        data = {}
        response = self.client.delete(self.url + "2/", data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)

    # invalid key
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_invalid_key(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'password',
        }

        response = self.client.delete(self.url + "1/", data=data, headers=utils.get_auth_header_invalid())
        self.assertEqual(utils.HTTP_UNAUTHORIZED, response.status_code)

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)

    # already deleted account
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_already_deleted(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'password',
        }

        # initial delete
        response = self.client.delete(self.url + "2/", data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_OK, response.status_code)

        user_count_mid = User.objects.all().count()
        self.assertEqual(user_count_start - 1, user_count_mid)

        # try deleting again
        response = self.client.delete(self.url + "2/", data=data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_NOT_FOUND, response.status_code)

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start - 1, user_count_end)
