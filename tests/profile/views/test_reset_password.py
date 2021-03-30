from django.core import mail
from django import forms
from django.urls import reverse
from oppia.test import OppiaTestCase


class ResetPasswordTest(OppiaTestCase):

    demo_email_address = 'demo@me.com'
    url = reverse('password_reset')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')
        self.assertEqual(200, response.status_code)

    def test_no_username(self):
        data = {}
        self.client.post(self.url, data=data)
        self.assertRaises(forms.ValidationError)

    def test_empty_username(self):
        data = {'username': ''}
        self.client.post(self.url, data=data)
        self.assertRaises(forms.ValidationError)

    def test_invalid_username(self):
        data = {'username': 'invalidusername'}
        self.client.post(self.url, data=data)
        self.assertRaises(forms.ValidationError)

    def test_valid_username(self):
        data = {'email': 'demo'}
        self.client.post(self.url, data=data)
        self.assertRaises(forms.ValidationError)
        self.assertEqual(len(mail.outbox), 0)
        mail.outbox = []

    def test_valid_email(self):
        data = {'email': self.demo_email_address}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response,
                             reverse('password_reset_done'),
                             302,
                             200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.demo_email_address)
        mail.outbox = []
