import unittest
import pytest
import json

from rest_framework.test import APITestCase

from tests.api.v3 import utils


class LeaderboardAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_leaderboard.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/usercoursesummary/course_tracker_v3.json']

    url = "/api/v3/leaderboard/"

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

    # check top user
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position1_user(self):
        auth_header = utils.make_auth_header("user4847", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(21, len(json_data['leaderboard']))

        leader = json_data['leaderboard'][0]
        self.assertTrue('position' in leader)
        self.assertTrue('username' in leader)
        self.assertTrue('first_name' in leader)
        self.assertTrue('last_name' in leader)
        self.assertTrue('points' in leader)
        self.assertTrue('badges' in leader)

        self.assertEqual(1, leader['position'])
        self.assertEqual("user4847", leader['username'])
        self.assertEqual("User", leader['first_name'])
        self.assertEqual("4847", leader['last_name'])
        self.assertEqual(169437, leader['points'])
        self.assertEqual(7, leader['badges'])

    # Check bottom of top users
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position20_user(self):
        auth_header = utils.make_auth_header("user3263", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(40, len(json_data['leaderboard']))

        position_x = json_data['leaderboard'][37]
        self.assertTrue('position' in position_x)
        self.assertTrue('username' in position_x)
        self.assertTrue('first_name' in position_x)
        self.assertTrue('last_name' in position_x)
        self.assertTrue('points' in position_x)
        self.assertTrue('badges' in position_x)

        self.assertEqual(38, position_x['position'])
        self.assertEqual("user2622", position_x['username'])
        self.assertEqual("User", position_x['first_name'])
        self.assertEqual("2622", position_x['last_name'])
        self.assertEqual(8446, position_x['points'])
        self.assertEqual(7, position_x['badges'])

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position21_user(self):
        auth_header = utils.make_auth_header("user3342", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(41, len(json_data['leaderboard']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position40_user(self):
        auth_header = utils.make_auth_header("user4351", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(60, len(json_data['leaderboard']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position100_user(self):
        auth_header = utils.make_auth_header("user2937", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(61, len(json_data['leaderboard']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position2000_user(self):
        auth_header = utils.make_auth_header("user4398", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(61, len(json_data['leaderboard']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position2017_user(self):
        auth_header = utils.make_auth_header("user4234", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(60, len(json_data['leaderboard']))

    # position 2037 is last
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_leaderboard_filtered_position2037_user(self):
        auth_header = utils.make_auth_header("user3169", "1234")
        response = self.client.get(self.url, headers=auth_header)
        self.assertEqual(response.status_code, utils.HTTP_OK)

        json_data = response.json()
        self.assertTrue('leaderboard' in json_data)
        self.assertEqual(40, len(json_data['leaderboard']))
