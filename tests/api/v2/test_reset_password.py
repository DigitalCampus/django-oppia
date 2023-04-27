from django.core import mail
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from tests.utils import get_api_url


class ResetPasswordResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json']
    demo_email_address = 'demo@me.com'

    def setUp(self):
        super(ResetPasswordResourceTest, self).setUp()
        self.url = get_api_url('v2', 'reset')

    # check get method not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url, format='json'))

    def test_no_username(self):
        data = {}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 0)

    def test_empty_username(self):
        data = {'username': ''}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_username(self):
        data = {'username': 'invalidusername'}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_username(self):
        data = {'username': 'demo'}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        response_data = self.deserialize(resp)
        self.assertTrue('message' in response_data)
        self.assertTrue('username' in response_data)
        self.assertEqual('demo', response_data['username'])
        self.assertFalse('password' in response_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.demo_email_address)
        mail.outbox = []

    def test_valid_email(self):
        data = {'username': self.demo_email_address}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        response_data = self.deserialize(resp)
        self.assertTrue('message' in response_data)
        self.assertTrue('username' in response_data)
        self.assertEqual('demo@me.com', response_data['username'])
        self.assertFalse('password' in response_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.demo_email_address)
        mail.outbox = []
