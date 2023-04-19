import json

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class PointsResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_leaderboard.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/usercoursesummary/course_tracker_v3.json']

    STR_LEADERBOARD_FILTERED_URL = "/api/v2/leaderboard/"

    # check get not allowed
    def test_get_unauthorized(self):
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'points')
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json'))

    # check post not allowed
    def test_post_not_allowed(self):
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'points')
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # check get with an invalid apiKey
    def test_get_apikeyinvalid(self):
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'points')
        auth_header = self.create_apikey(username=self.username, api_key="badbadbad")
        self.assertHttpUnauthorized(
            self.api_client.get(self.url,
                                format='json',
                                authentication=auth_header))

    # check a valid get
    def test_get_points(self):
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        auth_header = self.create_apikey(username=user.username, api_key=api_key.key)
        self.url = get_api_url('v2', 'points')
        resp = self.api_client.get(self.url, format='json', authentication=auth_header)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        points = self.deserialize(resp)['objects']

        self.assertEqual(12, len(points))
        point = points[0]
        self.assertTrue('date' in point)
        self.assertTrue('description' in point)
        self.assertTrue('points' in point)
        self.assertTrue('type' in point)

    def test_get_leaderboard_all(self):
        auth_header = self.create_apikey(username="user4996", api_key="1234")
        response = self.api_client.get('/api/v2/leaderboard-all/', format='json', authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)

        self.assertTrue('generated_date' in json_data)
        self.assertTrue('server' in json_data)
        self.assertTrue('leaderboard' in json_data)

        self.assertEqual(2037, len(json_data['leaderboard']))

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

        position567 = json_data['leaderboard'][566]
        self.assertEqual(567, position567['position'])
        self.assertEqual("user4856", position567['username'])
        self.assertEqual("User", position567['first_name'])
        self.assertEqual("4856", position567['last_name'])
        self.assertEqual(720, position567['points'])
        self.assertEqual(1, position567['badges'])

    # check top user
    def test_get_leaderboard_filtered_position1_user(self):
        auth_header = self.create_apikey(username="user4847", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
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
    def test_get_leaderboard_filtered_position20_user(self):
        auth_header = self.create_apikey(username="user3263", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
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

    def test_get_leaderboard_filtered_position21_user(self):
        auth_header = self.create_apikey(username="user3342", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(41, len(json_data['leaderboard']))

    def test_get_leaderboard_filtered_position40_user(self):
        auth_header = self.create_apikey(username="user4351", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(60, len(json_data['leaderboard']))

    def test_get_leaderboard_filtered_position100_user(self):
        auth_header = self.create_apikey(username="user2937", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(61, len(json_data['leaderboard']))

    def test_get_leaderboard_filtered_position2000_user(self):
        auth_header = self.create_apikey(username="user4398", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(61, len(json_data['leaderboard']))

    def test_get_leaderboard_filtered_position2017_user(self):
        auth_header = self.create_apikey(username="user4234", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(60, len(json_data['leaderboard']))

    # position 2037 is last
    def test_get_leaderboard_filtered_position2037_user(self):
        auth_header = self.create_apikey(username="user3169", api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(40, len(json_data['leaderboard']))
