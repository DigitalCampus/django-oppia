import unittest
import pytest

from rest_framework.test import APITestCase

from tests.api.v3 import utils


class BadgeAPITests(APITestCase):
    fixtures = ['default_badges.json']

    url = '/api/v3/badge/'

    # check post not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_post_invalid(self):
        response = self.client.post(self.url, data={}, headers=utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # check delete not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_delete_invalid(self):
        response = self.client.delete(self.url, data={}, headers=utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # check unauthorized
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_unauthorized(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_invalid())
        self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

    # check correct
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_correct(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())

        self.assertEqual(response.status_code, utils.HTTP_OK)
        # check that the response contains 1 badge
        self.assertEqual(len(response.json()), 1)

        badge = response.json()[0]
        self.assertTrue('allow_multiple_awards' in badge)
        self.assertTrue('default_icon' in badge)
        self.assertTrue('description' in badge)
        self.assertTrue('id' in badge)
        self.assertTrue('name' in badge)
        self.assertTrue('points' in badge)
        self.assertTrue('ref' in badge)
