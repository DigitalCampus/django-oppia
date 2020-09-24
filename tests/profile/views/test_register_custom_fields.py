from django.core.exceptions import ValidationError
from django.urls import reverse
from oppia.test import OppiaTestCase

from profile.models import CustomField, UserProfileCustomField


class RegisterCustomFieldsViewTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_course_permissions.json']
    base_filled_form = {
            'username': 'new_username',
            'email': 'newusername@email.com',
            'password': 'password',
            'password_again': 'password',
            'first_name': 'Test name',
            'last_name': 'Last name'
        }

    def setUp(self):
        super(RegisterCustomFieldsViewTest, self).setUp()
        self.url = reverse('profile:register')
        self.thanks_url = reverse('profile:register_thanks')

    # INTEGER REQUIRED
    # with int in form - correct
    def test_int_required_field_with_int(self):
        custom_field = CustomField(
            id='int_req',
            label='Integer required',
            required=True,
            type='int')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['int_req'] = 123
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        # check saved to value_int field
        saved_row = UserProfileCustomField.objects.latest('created')
        self.assertEqual(saved_row.value_int, 123)

    # without int in form - invalid
    def test_int_required_field_without_int(self):
        custom_field = CustomField(
            id='int_req',
            label='Integer required',
            required=True,
            type='int')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()
        self.client.post(self.url, data=self.base_filled_form)
        self.assertRaises(ValidationError)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # INTEGER NOT REQUIRED
    # with int in form - correct
    def test_int_not_required_field_with_int(self):
        custom_field = CustomField(
            id='int_not_req',
            label='Integer not required',
            required=False,
            type='int')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['int_not_req'] = 123
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        # check saved to value_int field
        saved_row = UserProfileCustomField.objects.latest('created')
        self.assertEqual(saved_row.value_int, 123)

    # without int in form - correct
    def test_int_not_required_field_without_int(self):
        custom_field = CustomField(
            id='int_not_req',
            label='Integer not required',
            required=False,
            type='int')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        resp = self.client.post(self.url, data=self.base_filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # BOOLEAN REQUIRED
    # with bool in form - correct
    def test_bool_required_field_with_bool_true(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['bool_req'] = True
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        # check saved to value_int field
        saved_row = UserProfileCustomField.objects.latest('created')
        self.assertEqual(saved_row.value_bool, True)

    def test_bool_required_field_with_bool_false(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['bool_req'] = False
        count_start = UserProfileCustomField.objects.all().count()
        self.client.post(self.url, data=filled_form)
        self.assertRaises(ValidationError)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # without int in form - invalid
    def test_bool_required_field_without_bool(self):
        custom_field = CustomField(
            id='bool_req',
            label='Boolean required',
            required=True,
            type='bool')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()
        self.client.post(self.url, data=self.base_filled_form)
        self.assertRaises(ValidationError)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # BOOLEAN NOT REQUIRED
    # with bool in form - correct
    def test_bool_not_required_field_with_bool_true(self):
        custom_field = CustomField(
            id='bool_not_req',
            label='Boolean not required',
            required=False,
            type='bool')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['bool_not_req'] = True
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        # check saved to value_bool field
        saved_row = UserProfileCustomField.objects.latest('created')
        self.assertEqual(saved_row.value_bool, True)

    def test_bool_not_required_field_with_bool_false(self):
        custom_field = CustomField(
            id='bool_not_req',
            label='Boolean not required',
            required=False,
            type='bool')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['bool_not_req'] = False
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        # check saved to value_bool field
        saved_row = UserProfileCustomField.objects.latest('created')
        self.assertEqual(saved_row.value_bool, False)

    # without bool in form - correct
    def test_bool_not_required_field_without_bool(self):
        custom_field = CustomField(
            id='bool_not_req',
            label='Boolean not required',
            required=False,
            type='bool')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        resp = self.client.post(self.url, data=self.base_filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

    # STRING REQUIRED
    # with str in form - correct
    def test_str_required_field_with_str(self):
        custom_field = CustomField(
            id='str_req',
            label='String required',
            required=True,
            type='str')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['str_req'] = "my string"
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        # check saved to value_int field
        saved_row = UserProfileCustomField.objects.latest('created')
        self.assertEqual(saved_row.value_str, "my string")

    def test_str_required_field_with_str_blank(self):
        custom_field = CustomField(
            id='str_req',
            label='String required',
            required=True,
            type='str')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['str_req'] = ""
        count_start = UserProfileCustomField.objects.all().count()
        self.client.post(self.url, data=filled_form)
        self.assertRaises(ValidationError)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # without int in form - invalid
    def test_str_required_field_without_str(self):
        custom_field = CustomField(
            id='str_req',
            label='String required',
            required=True,
            type='str')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()
        self.client.post(self.url, data=self.base_filled_form)
        self.assertRaises(ValidationError)
        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # STRING NOT REQUIRED
    # with str in form - correct
    def test_str_not_required_field_with_str_true(self):
        custom_field = CustomField(
            id='str_not_req',
            label='String not required',
            required=False,
            type='str')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['str_not_req'] = "my string"
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start+1, count_end)

        # check saved to value_str field
        saved_row = UserProfileCustomField.objects.latest('created')
        self.assertEqual(saved_row.value_str, "my string")

    def test_str_not_required_field_with_str_blank(self):
        custom_field = CustomField(
            id='str_not_req',
            label='String not required',
            required=False,
            type='str')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        # with int in form - correct
        filled_form = self.base_filled_form.copy()
        filled_form['str_not_req'] = ""
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)

    # without str in form - correct
    def test_str_not_required_field_without_str(self):
        custom_field = CustomField(
            id='str_not_req',
            label='String not required',
            required=False,
            type='str')
        custom_field.save()

        count_start = UserProfileCustomField.objects.all().count()

        resp = self.client.post(self.url, data=self.base_filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

        count_end = UserProfileCustomField.objects.all().count()
        self.assertEqual(count_start, count_end)
