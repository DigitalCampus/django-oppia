from django.contrib.auth.models import User
from django.test import TestCase

from tastypie.exceptions import Unauthorized
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class ProfileUpdatePermissionsResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(ProfileUpdatePermissionsResourceTest, self).setUp()
        self.username = 'demo'
        self.user = User.objects.get(username=self.username)
        self.api_key = get_api_key(user=self.user).key
        self.base_data = {
            'email': 'demo@me.com',
            'first_name': 'demo',
            'last_name': 'user',
            'organisation': ''
        }
        self.url = get_api_url('v2', 'profileupdate')

    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)

    # Get invalid
    def test_get_invalid(self):
        response = self.client.get(self.url,
                                   authentication=self.get_credentials())
        self.assertEqual(response.status_code, 405)

    # test unauthorized
    def test_unauthorized_badpassword(self):
        auth = self.create_apikey(username=self.username, api_key="1234")
        response = self.api_client.post(self.url,
                                        format='json',
                                        data=self.base_data,
                                        authentication=auth)
        self.assertHttpUnauthorized(response)

    # test authorized
    def test_authorized(self):
        response = self.api_client.post(self.url,
                                        format='json',
                                        data=self.base_data,
                                        authentication=self.get_credentials())
        self.assertHttpCreated(response)

    # cannot edit another user
    def test_cannot_edit_other_user(self):
        post_data = self.base_data.copy()
        post_data['username'] = 'admin'

        with self.assertRaises(Unauthorized):
            self.api_client.post(self.url,
                                 format='json',
                                 data=post_data,
                                 authentication=self.get_credentials())
