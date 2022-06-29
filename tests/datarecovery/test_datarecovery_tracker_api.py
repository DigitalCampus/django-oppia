

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from datarecovery.models import DataRecovery
from tests.utils import get_api_key, get_api_url


class TrackerResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json',
                'tests/test_tracker.json']

    def setUp(self):
        super(TrackerResourceTest, self).setUp()
        self.username = 'demo'
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'tracker')

    def get_credentials(self):
        return self.create_apikey(username=self.username,
                                  api_key=self.api_key)

    def test_bad_auth(self):
        pass

    def test_all_info_correct(self):
        pass


    def wrong_tracker_data_format(self):
        pass

    def test_malformed_tracker(self):
        wrong_data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',  # page
            'data': '{\"uuid\": this is not a valid JSON}'
        }

        datacount_start = DataRecovery.objects.count()
        resp = self.api_client.post(self.url,
                                    data=wrong_data, format='json',
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertEqual(datacount_start + 1, DataRecovery.objects.count())

        last_data = DataRecovery.objects.all().latest('pk')
        self.assertTrue(DataRecovery.Reason.JSON_DECODE_ERROR in last_data.reasons)
