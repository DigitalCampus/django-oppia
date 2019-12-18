
from django import forms
from django.test import TestCase

from profile.forms.reset import ResetForm

class ProfileFormResetTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(ProfileFormResetTest, self).setUp()

    def test_no_data(self):
        form = ResetForm()
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = ResetForm({'username': ''})
        self.assertFalse(form.is_valid())
        self.assertRaises(forms.ValidationError)

    def test_invalid_username(self):
        form = ResetForm({'username': 'invaliduser'})
        self.assertFalse(form.is_valid())
        self.assertRaises(forms.ValidationError)

    def test_invalid_email(self):
        form = ResetForm({'username': 'invaliduser@email.com'})
        self.assertFalse(form.is_valid())
        self.assertRaises(forms.ValidationError)

    def test_valid_username(self):
        form = ResetForm({'username': 'admin'})
        self.assertTrue(form.is_valid())

    def test_valid_email(self):
        form = ResetForm({'username': 'admin@me.com'})
        self.assertTrue(form.is_valid())
        