import unittest
import pytest
import json

from rest_framework.test import APITestCase

from tests.api.v3 import utils


class PointsAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_leaderboard.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/usercoursesummary/course_tracker_v3.json']

    url = "/api/v3/points/"

    # check post not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_post_invalid(self):
        response = self.client.post(self.url,
                                    data=json.dumps({}),
                                    content_type="application/json",
                                    headers=utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # check put not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_put_invalid(self):
        response = self.client.put(self.url,
                                   data=json.dumps({}),
                                   content_type="application/json",
                                   headers=utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # check delete not allowed
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_delete_invalid(self):
        response = self.client.delete(self.url, headers=utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    # check a valid get
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_admin(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_admin())

        self.assertEqual(response.status_code, utils.HTTP_OK)

        points = response.json()
        self.assertEqual(12, len(points))  # actual value tested might need to be updated here
        point = points[0]
        self.assertTrue('date' in point)
        self.assertTrue('description' in point)
        self.assertTrue('points' in point)
        self.assertTrue('type' in point)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_staff(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_staff())

        self.assertEqual(response.status_code, utils.HTTP_OK)

        points = response.json()
        self.assertEqual(12, len(points))  # actual value tested might need to be updated here
        point = points[0]
        self.assertTrue('date' in point)
        self.assertTrue('description' in point)
        self.assertTrue('points' in point)
        self.assertTrue('type' in point)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_teacher(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_teacher())

        self.assertEqual(response.status_code, utils.HTTP_OK)

        points = response.json()
        self.assertEqual(12, len(points))  # actual value tested might need to be updated here
        point = points[0]
        self.assertTrue('date' in point)
        self.assertTrue('description' in point)
        self.assertTrue('points' in point)
        self.assertTrue('type' in point)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_user(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())

        self.assertEqual(response.status_code, utils.HTTP_OK)

        points = response.json()
        self.assertEqual(12, len(points))  # 12 should be correct
        point = points[0]
        self.assertTrue('date' in point)
        self.assertTrue('description' in point)
        self.assertTrue('points' in point)
        self.assertTrue('type' in point)
