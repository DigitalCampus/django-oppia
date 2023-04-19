import json

from django.contrib.auth.models import User

from tests.profile.user_profile_base_test_case import UserProfileBaseTestCase


class ProfileUpdateResourceTest(UserProfileBaseTestCase):

    def test_edit_own_profile_user(self):
        orig_firstname = self.user.first_name
        new_firstname = 'Hernan'

        orig_lastname = self.user.last_name
        new_lastname = 'Cortez'

        orig_org = self.user.userprofile.organisation
        new_org = 'my organisation'

        post_data = self.base_data.copy()
        post_data['first_name'] = new_firstname
        post_data['last_name'] = new_lastname
        post_data['organisation'] = new_org

        response = self.api_client.post(self.url,
                                        format='json',
                                        data=post_data,
                                        authentication=self.get_credentials())
        self.assertHttpCreated(response)

        self.assertValidJSON(response.content)
        json_data = json.loads(response.content)

        self.assertTrue('email' in json_data)
        self.assertTrue('first_name' in json_data)
        self.assertTrue('last_name' in json_data)
        self.assertTrue('organisation' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("Hernan", json_data['first_name'])
        self.assertEqual("Cortez", json_data['last_name'])
        self.assertEqual("my organisation", json_data['organisation'])

        updated_user = User.objects.get(username=self.username)
        self.assertNotEqual(orig_firstname, updated_user.first_name)
        self.assertNotEqual(orig_lastname, updated_user.last_name)
        self.assertNotEqual(orig_org, updated_user.userprofile.organisation)
