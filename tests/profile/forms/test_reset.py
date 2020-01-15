
from django import forms
from oppia.test import OppiaTestCase

from profile.forms.reset import ResetForm


class ProfileFormResetTest(OppiaTestCase):

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
