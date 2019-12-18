from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class ProfileUpdateResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(ProfileUpdateResourceTest, self).setUp()
        self.username = 'demo'
        self.user = User.objects.get(username=self.username)
        self.api_key = get_api_key(user=self.user).key
        self.base_data = {
            'email': 'demo@me.com',
            'firstname': 'demo',
            'lastname': 'user',
            'organisation': ''
        }
        self.url = get_api_url('profileupdate')

    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)

    def test_edit_own_profile_user(self):
        orig_firstname = self.user.first_name
        new_firstname = 'Hernan'

        orig_lastname = self.user.last_name
        new_lastname = 'Cortez'

        orig_org = self.user.userprofile.organisation
        new_org = 'my organisation'

        post_data = self.base_data.copy()
        post_data['firstname'] = new_firstname
        post_data['lastname'] = new_lastname
        post_data['organisation'] = new_org

        response = self.api_client.post(self.url,
                                        format='json',
                                        data=post_data,
                                        authentication=self.get_credentials())
        self.assertHttpCreated(response)

        updated_user = User.objects.get(username=self.username)
        self.assertNotEqual(orig_firstname, updated_user.first_name)
        self.assertNotEqual(orig_lastname, updated_user.last_name)
        self.assertNotEqual(orig_org, updated_user.userprofile.organisation)
