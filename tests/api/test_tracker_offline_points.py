# oppia/tests/api/test_tracker_offline_points.py

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Tracker, Points
from tests.utils import get_api_key, get_api_url


class TrackerResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json']

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
            'digest': '11cc12291f730160c324b727dd2268b612137',
            'points': 500,
            'event': 'activity_completed',
            'completed': 1,
        }
        tracker_count_start = Tracker.objects.all().count()
        points_count_start = Points.objects.all().count()

        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        # check the tracker record was successfully added
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)

        # Check tracker includes the points and event data
        latest_tracker = Tracker.objects.latest('submitted_date')

        self.assertEqual(latest_tracker.points, 500)
        self.assertEqual(latest_tracker.event, 'activity_completed')

        # check that the points info has been added
        points_count_end = Points.objects.all().count()
        self.assertEqual(points_count_start + 1, points_count_end)

        latest_points = Points.objects.latest('date')

        self.assertEqual(latest_points.points, 500)
        self.assertEqual(latest_points.type, 'activity_completed')

        # check that all data is there
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        self.assertTrue('completed' in response_data)
        self.assertTrue(response_data['completed'])

    # test when points are not included in tracker
    def test_post_points_not_included(self):
        data = {
            'digest': '11cc12291f730160c324b727dd2268b612137',
            'completed': 1
        }
        tracker_count_start = Tracker.objects.all().count()
        points_count_start = Points.objects.all().count()

        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        # check the record was successfully added
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)

        latest_tracker = Tracker.objects.latest('submitted_date')
        self.assertEqual(latest_tracker.digest, '11cc12291f730160c324b727dd2268b612137')

        # check that the points info has been added
        points_count_end = Points.objects.all().count()
        self.assertEqual(points_count_start + 1, points_count_end)

        latest_points = Points.objects.latest('date')

        self.assertEqual(latest_points.points, 10)
        self.assertEqual(latest_points.type, 'activity_completed')

        # check that all data is there
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        self.assertTrue('completed' in response_data)
        self.assertTrue(response_data['completed'])
