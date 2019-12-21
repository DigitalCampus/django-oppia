from django.core import mail
from django import forms
from django.urls import reverse
from oppia.test import OppiaTestCase


class ResetPasswordTest(OppiaTestCase):
    
    demo_email_address = 'demo@me.com'
    url = reverse('profile_reset')


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
        data = {'username': 'demo'}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response,
                             reverse('profile_reset_sent'),
                             302,
                             200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.demo_email_address)
        mail.outbox = []

    def test_valid_email(self):
        data = {'username': self.demo_email_address}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response,
                             reverse('profile_reset_sent'),
                             302,
                             200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.demo_email_address)
        mail.outbox = []
    