
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from tests.utils import get_api_url

class UsernameReminderResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json']
    demo_email_address = 'demo@me.com'


    def setUp(self):
        super(UsernameReminderResourceTest, self).setUp()
        self.url = get_api_url('v2', 'username')
        
    # get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url,
                                                            format='json'))

    # email not in post params
    def test_no_email(self):
        data = {}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 0)

    # email is blank
    def test_empty_email(self):
        data = {'email': ''}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 0)

    # email doesn't exist
    def test_email_doesnt_exist(self):
        data = {'email': 'dummy@email.com'}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 0)
        
    # multiple users with same email
    def test_email_multiple(self):
        user = User(email='admin@me.com', username='anotheradmin', password='dummypassword')
        user.save()
        data = {'email': 'admin@me.com'}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "admin@me.com")

    # correct (one valid email)
    def test_email_one_valid(self):
        data = {'email': 'staff@me.com'}
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "staff@me.com")