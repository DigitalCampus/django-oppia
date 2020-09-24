from django.core.exceptions import ValidationError
from django.urls import reverse
from oppia.test import OppiaTestCase

from profile.models import CustomField, UserProfileCustomField


class ProfileEditCustomFieldsViewTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(ProfileEditCustomFieldsViewTest, self).setUp()
        self.url = reverse('profile:edit')

    def test_edit_profile_no_data(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()

        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name}
        count_start = UserProfileCustomField.objects.all().count()
        self.client.post(self.url, data=post_data)
        self.assertRaises(ValidationError)
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
                                      user=self.normal_user,
                                      value_bool=True)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'bool_req': False}
        count_start = UserProfileCustomField.objects.all().count()
        self.client.post(self.url, data=post_data)
        self.assertRaises(ValidationError)
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
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'bool_req': True}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_bool=True)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'bool_req': True}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_bool=True)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'bool_not_req': False}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_bool=True)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'bool_not_req': True}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_int=123)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'int_req': 999}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
        self.assertEqual(updated_row.value_int, 999)

    # new requirement or new field
    def test_edit_profile_req_int_new(self):
        custom_field = CustomField(
            id='int_req',
            label='Integer required',
            required=True,
            type='int')
        custom_field.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'int_req': 123}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
        self.assertEqual(updated_row.value_int, 123)

    # editing required int field - without change
    def test_edit_profile_req_int_no_change(self):
        custom_field = CustomField(
            id='int_req',
            label='Integer required',
            required=True,
            type='int')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.normal_user,
                                      value_int=123)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'int_req': 123}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_int=123)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'int_not_req': 1234}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_int=123)
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'int_not_req': 123}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_str="my string")
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'str_req': "my new string"}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
        self.assertEqual(updated_row.value_str, "my new string")

    # new requirement or new field
    def test_edit_profile_req_str_new(self):
        custom_field = CustomField(
            id='str_req',
            label='String required',
            required=True,
            type='str')
        custom_field.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'str_req': "my new string"}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_str="my string")
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'str_req': "my string"}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_str="my string")
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'str_not_req': "my new string"}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
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
                                      user=self.normal_user,
                                      value_str="my string")
        upcf.save()
        self.client.force_login(self.normal_user)
        post_data = {'organisation': self.normal_user.userprofile.organisation,
                     'email': self.normal_user.email,
                     'username': self.normal_user.username,
                     'first_name': self.normal_user.first_name,
                     'last_name': self.normal_user.last_name,
                     'str_not_req': "my string"}
        count_start = UserProfileCustomField.objects.all().count()
        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

        updated_row = UserProfileCustomField.objects.get(key_name=custom_field,
                                                         user=self.normal_user)
        self.assertEqual(updated_row.value_str, "my string")
