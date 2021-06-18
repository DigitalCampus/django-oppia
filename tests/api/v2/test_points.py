import json

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class PointsResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_leaderboard.json'
                ]

    STR_LEADERBOARD_FILTERED_URL = "/api/v2/leaderboard/"

    # check get not allowed
    def test_get_unauthorized(self):
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'points')
        self.assertHttpUnauthorized(self.api_client.get(self.url,
                                                        format='json'))

    # check post not allowed
    def test_post_not_allowed(self):
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'points')
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url,
                                                             format='json',
                                                             data={}))

    # check get with an invalid apiKey
    def test_get_apikeyinvalid(self):
        self.username = 'demo'
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'points')
        auth_header = self.create_apikey(username=self.username,
                                         api_key="badbadbad")
        self.assertHttpUnauthorized(
            self.api_client.get(self.url,
                                format='json',
                                authentication=auth_header))

    # check a valid get
    def test_get_points(self):
        auth_header = self.create_apikey(username="user4996",
                                         api_key="1234")
        self.url = get_api_url('v2', 'points')
        res = self.api_client.get(self.url,
                                  format='json',
                                  authentication=auth_header)
        self.assertHttpOK(res)
        self.assertValidJSON(res.content)

    def test_get_leaderboard_all(self):
        auth_header = self.create_apikey(username="user4996",
                                         api_key="1234")
        response = self.api_client.get('/api/v2/leaderboard-all/',
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(2037, len(json_data['leaderboard']))

    # check top user
    def test_get_leaderboard_filtered_position1_user(self):
        auth_header = self.create_apikey(username="user4847",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(21, len(json_data['leaderboard']))
        
    # Check bottom of top users
    def test_get_leaderboard_filtered_position20_user(self):
        auth_header = self.create_apikey(username="user3263",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(40, len(json_data['leaderboard']))

    def test_get_leaderboard_filtered_position21_user(self):
        auth_header = self.create_apikey(username="user3342",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(41, len(json_data['leaderboard']))
        
    def test_get_leaderboard_filtered_position40_user(self):
        auth_header = self.create_apikey(username="user4351",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(60, len(json_data['leaderboard']))

    def test_get_leaderboard_filtered_position100_user(self):
        auth_header = self.create_apikey(username="user2937",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(61, len(json_data['leaderboard']))
    
    def test_get_leaderboard_filtered_position2000_user(self):
        auth_header = self.create_apikey(username="user4398",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(61, len(json_data['leaderboard'])) 
          
    def test_get_leaderboard_filtered_position2017_user(self):
        auth_header = self.create_apikey(username="user4234",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)    
        self.assertEqual(60, len(json_data['leaderboard']))  
        
    # position 2037 is last
    def test_get_leaderboard_filtered_position2037_user(self):
        auth_header = self.create_apikey(username="user3169",
                                         api_key="1234")
        response = self.api_client.get(self.STR_LEADERBOARD_FILTERED_URL,
                                       format='json',
                                       authentication=auth_header)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)
        self.assertEqual(40, len(json_data['leaderboard']))
