from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import TestCase

from profile.models import CustomField, UserProfileCustomField
from settings import constants
from settings.models import SettingProperties


class RegisterCustomFieldsViewTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json']
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
        self.url = reverse('profile_register')
        self.thanks_url = reverse('profile_register_thanks')

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

        
# bool req
# bool not req
# str req
# str not req
