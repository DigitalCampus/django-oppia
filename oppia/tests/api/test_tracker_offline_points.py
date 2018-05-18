# oppia/tests/api/test_tracker_offline_points.py

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Tracker
from oppia.tests.utils import get_api_key, get_api_url


class TrackerResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['user.json', 'oppia.json']

    def setUp(self):
        super(TrackerResourceTest, self).setUp()
        self.username = 'demo'
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('tracker')
     
    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)
    
    # test when points are included in tracker
    def test_post_points_included(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
            'points': 500
        }
        tracker_count_start = Tracker.objects.all().count()
        points_count_start = Points.objects.all().count()
        
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        
        # check the tracker record was successfully added
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

        # check that the points info has been added

        
        
        # check that all data is there
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        self.assertTrue('completed' in response_data)
        self.assertFalse(response_data['completed'])   
        
    # test when points are not included in tracker
    def test_post_points_not_included(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
        }
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        # check the record was succesfully added
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

        # check that all data is there
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        self.assertTrue('completed' in response_data)
        self.assertFalse(response_data['completed']) 
    