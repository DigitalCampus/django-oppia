# oppia/tests/api/test_tracker.py

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

    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url))

    # test unauthorized
    def test_unauthorized(self):
        data = {
            'digest': '123456789123456789',
        }
        bad_auth = self.create_apikey(username=self.username, api_key="1234")
        self.assertHttpUnauthorized(self.api_client.post(self.url, format='json', data=data, authentication=bad_auth))

    # check put not allowed
    def test_put_invalid(self):
        resource_url = get_api_url('tracker', 1)
        self.assertHttpMethodNotAllowed(self.api_client.put(resource_url))

    # test what happens when the digest is not found
    # should still add the record
    def test_post_digest_not_found(self):
        data = {
            'digest': '123456789123456789',
        }
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)
        self.assertValidJSON(resp.content)

    # test when digest is valid
    def test_post_digest_found(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
        }
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        # check the record was successfully added
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)

        # check that all data is there
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        self.assertTrue('completed' in response_data)
        self.assertFalse(response_data['completed'])

    # check existing trackers can't be overwritten
    def test_post_no_overwrite(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
        }
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
        }
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)

    def test_patch_all_valid_digests(self):
        activity1 = {
            'digest': '18ec12e5653a40431f453cce35811fa4',        # page
        }
        activity2 = {
            'digest': '3ec4d8ab03c3c6bd66b3805f0b11225b',        # media
        }
        activity3 = {
            'digest': '74ff568f95ddcfeb4ac809012eea7b5e',        # quiz
        }

        data = {'objects': [activity1, activity2, activity3]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 3, tracker_count_end)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)

    def test_patch_all_invalid_digests(self):
        activity1 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d',        # invalid
        }
        activity2 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d',        # invalid
        }
        activity3 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d',        # invalid
        }

        data = {'objects': [activity1, activity2, activity3]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 3, tracker_count_end)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)

    def test_patch_mix_invalid_valid_digests(self):
        activity1 = {
            'digest': '18ec12e5653a40431f453cce35811fa4',        # page
        }
        activity2 = {
            'digest': '3ec4d8ab03c3c6bd66b3805f0b11225b',        # media
        }
        activity3 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d',        # quiz
        }

        data = {'objects': [activity1, activity2, activity3]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 3, tracker_count_end)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        
    def test_patch_unique_uuid(self):
        activity1 = {
            'digest': '18ec12e5653a40431f453cce35811fa4',  # page
            'data': '{\"uuid\": \"d5f305e9-dd03-4d97-96d5-5a3c45169e02\"}'
        }
        activity2 = {
            'digest': '3ec4d8ab03c3c6bd66b3805f0b11225b',  # media
            'data': '{\"uuid\": \"baa673cb-e5fc-4797-b7e9-58a06ed80915\"}'
        }

        data = {'objects': [activity1, activity2]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)

    def test_patch_duplicate_uuid(self):
        activity1 = {
            'digest': '18ec12e5653a40431f453cce35811fa4',  # page
            'data': '{\"uuid\": \"d5f305e9-dd03-4d97-96d5-5a3c45169e02\"}'
        }
        activity2 = {
            'digest': '18ec12e5653a40431f453cce35811fa4',  # page
            'data': '{\"uuid\": \"d5f305e9-dd03-4d97-96d5-5a3c45169e02\"}'
        }

        data = {'objects': [activity1, activity2]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)

    def test_post_unique_uuid(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',  # page
            'data': '{\"uuid\": \"d5f305e9-dd03-4d97-96d5-5a3c45169e02\"}'
        }

        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)

    def test_post_duplicate_uuid(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',  # page
            'data': '{\"uuid\": \"d5f305e9-dd03-4d97-96d5-5a3c45169e02\"}'
        }

        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)

        # send the same again
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)
