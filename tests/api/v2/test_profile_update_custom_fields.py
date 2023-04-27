import json

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url

from profile.models import CustomField, UserProfileCustomField


class ProfileEditCustomFieldsViewTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json']

    def setUp(self):
        super(ProfileEditCustomFieldsViewTest, self).setUp()
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

    def test_edit_profile_no_data(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()
        response = self.api_client.post(self.url,
                                        format='json',
                                        data=self.base_data,
                                        authentication=self.get_credentials())
        self.assertHttpBadRequest(response)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # BOOLEAN REQUIRED
    # editing required bool field - with change
    def test_edit_profile_req_bool_change(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_bool=True)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['bool_req'] = False
        count_start = UserProfileCustomField.objects.all().count()
        response = self.api_client.post(self.url,
                                        format='json',
                                        data=post_data,
                                        authentication=self.get_credentials())
        self.assertHttpBadRequest(response)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # new requirement or new field
    def test_edit_profile_req_bool_new(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()

        post_data = self.base_data.copy()
        post_data['bool_req'] = True
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('bool_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(True, json_data['bool_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_bool, True)

    # editing required bool field - without change
    def test_edit_profile_req_bool_no_change(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()

        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_bool=True)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['bool_req'] = True
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('bool_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(True, json_data['bool_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_bool, True)

    # BOOLEAN NOT REQUIRED
    # editing not required bool field - with change
    def test_edit_profile_not_req_bool_change(self):
        custom_field = CustomField(
            id='bool_not_req',
            label='Boolean not required',
            required=False,
            type='bool')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_bool=True)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['bool_not_req'] = False
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('bool_not_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(False, json_data['bool_not_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_bool, False)

    # editing not required bool field - without change
    def test_edit_profile_not_req_bool_no_change(self):
        custom_field = CustomField(
            id='bool_not_req',
            label='Boolean not required',
            required=False,
            type='bool')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_bool=True)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['bool_not_req'] = True
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('bool_not_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(True, json_data['bool_not_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_bool, True)

    # INTEGER REQUIRED
    # editing required int field - with change
    def test_edit_profile_req_int_change(self):
        custom_field = CustomField(
            id='int_req',
            label='Integer required',
            required=True,
            type='int')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_int=123)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['int_req'] = 999
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('int_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(999, json_data['int_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_int, 999)

    # new requirement or new field
    def test_edit_profile_req_int_new(self):
        custom_field = CustomField(
            id='int_req',
            label='Integer required',
            required=True,
            type='int')
        custom_field.save()
        post_data = self.base_data.copy()
        post_data['int_req'] = 999
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('int_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(999, json_data['int_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_int, 999)

    # editing required int field - without change
    def test_edit_profile_req_int_no_change(self):
        custom_field = CustomField(
            id='int_req',
            label='Integer required',
            required=True,
            type='int')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_int=123)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['int_req'] = 123
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('int_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(123, json_data['int_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_int, 123)

    # Integer NOT REQUIRED
    # editing not required int field - with change
    def test_edit_profile_not_req_int_change(self):
        custom_field = CustomField(
            id='int_not_req',
            label='Integer not required',
            required=False,
            type='int')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_int=123)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['int_not_req'] = 1234
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('int_not_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(1234, json_data['int_not_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_int, 1234)

    # editing not required int field - without change
    def test_edit_profile_not_req_int_no_change(self):
        custom_field = CustomField(
            id='int_not_req',
            label='Integer not required',
            required=False,
            type='int')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_int=123)
        upcf.save()
        post_data = self.base_data.copy()
        post_data['int_not_req'] = 123
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('int_not_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual(123, json_data['int_not_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_int, 123)

    # STRING REQUIRED
    # editing required str field - with change
    def test_edit_profile_req_str_change(self):
        custom_field = CustomField(
            id='str_req',
            label='String required',
            required=True,
            type='str')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str="my string")
        upcf.save()
        post_data = self.base_data.copy()
        post_data['str_req'] = "my new string"
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('str_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual("my new string", json_data['str_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_str, "my new string")

    # new requirement or new field
    def test_edit_profile_req_str_new(self):
        custom_field = CustomField(
            id='str_req',
            label='String required',
            required=True,
            type='str')
        custom_field.save()
        post_data = self.base_data.copy()
        post_data['str_req'] = "my new string"
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('str_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual("my new string", json_data['str_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_str, "my new string")

    # editing required str field - without change
    def test_edit_profile_req_str_no_change(self):
        custom_field = CustomField(
            id='str_req',
            label='String required',
            required=True,
            type='str')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str="my string")
        upcf.save()
        post_data = self.base_data.copy()
        post_data['str_req'] = "my string"
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('str_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual("my string", json_data['str_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_str, "my string")

    # String NOT REQUIRED
    # editing not required str field - with change
    def test_edit_profile_not_req_str_change(self):
        custom_field = CustomField(
            id='str_not_req',
            label='String not required',
            required=False,
            type='str')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str="my string")
        upcf.save()
        post_data = self.base_data.copy()
        post_data['str_not_req'] = "my new string"
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('str_not_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual("my new string", json_data['str_not_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_str, "my new string")

    # editing not required str field - without change
    def test_edit_profile_not_req_str_no_change(self):
        custom_field = CustomField(
            id='str_not_req',
            label='String not required',
            required=False,
            type='str')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str="my string")
        upcf.save()
        post_data = self.base_data.copy()
        post_data['str_not_req'] = "my string"
        count_start = UserProfileCustomField.objects.all().count()
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
        self.assertTrue('str_not_req' in json_data)

        self.assertEqual("demo@me.com", json_data['email'])
        self.assertEqual("demo", json_data['first_name'])
        self.assertEqual("user", json_data['last_name'])
        self.assertEqual("", json_data['organisation'])
        self.assertEqual("my string", json_data['str_not_req'])

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.user)
        self.assertEqual(updated_row.value_str, "my string")
