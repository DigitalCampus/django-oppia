
from datarecovery.models import DataRecovery
from tests.profile.user_profile_base_test_case import UserProfileBaseTestCase


class UserProfileResourceTest(UserProfileBaseTestCase):
    fixtures = UserProfileBaseTestCase.fixtures + ['tests/test_customfields.json', 'default_gamification_events.json']

    def test_correct_profile_update(self):

        initial_datacount = DataRecovery.objects.count()
        post_data = self.base_data.copy()
        response = self.api_client.post(self.url,
                                        format='json',
                                        data=post_data,
                                        authentication=self.get_credentials())
        self.assertHttpCreated(response)
        self.assertEqual(initial_datacount, DataRecovery.objects.count())


    # If we receive some fields not defined in the server, we should save them
    def test_missing_customfields(self):
        initial_datacount = DataRecovery.objects.count()
        post_data = self.base_data.copy()
        post_data['missing_customfield'] = 'test'
        response = self.api_client.post(self.url,
                                        format='json',
                                        data=post_data,
                                        authentication=self.get_credentials())
        self.assertHttpCreated(response)
        self.assertEqual(initial_datacount + 1, DataRecovery.objects.count())

        last_data = DataRecovery.objects.all().latest('pk')
        self.assertTrue(DataRecovery.Reason.CUSTOM_PROFILE_FIELDS_NOT_DEFINED_IN_THE_SERVER in last_data.reasons)
