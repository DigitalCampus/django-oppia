import unittest
import pytest

from rest_framework.test import APITestCase

from tests.api.v3 import utils


class AwardAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_course_permissions.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json',
                'tests/test_awardcourse.json']

    url = '/api/v3/award/'

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

    # check valid
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_valid(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())

        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(len(response.json()), 1)

        award = response.json()[0]
        self.assertTrue('certificate_pdf' in award)
        self.assertTrue('award_date' in award)
        self.assertTrue('badge_icon' in award)
        self.assertTrue('description' in award)
        self.assertTrue('badge' in award)
        self.assertTrue('emailed' in award)
        self.assertTrue('id' in award)
        self.assertTrue('validation_uuid' in award)

        badge = award['badge']
        self.assertTrue('allow_multiple_awards' in badge)
        self.assertTrue('default_icon' in badge)
        self.assertTrue('description' in badge)
        self.assertTrue('id' in badge)
        self.assertTrue('name' in badge)
        self.assertTrue('points' in badge)
        self.assertTrue('ref' in badge)

    # check returning a set of objects - expecting zero
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="incomplete api endpoint")
    def test_no_objects(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(len(response.json()), 0)
