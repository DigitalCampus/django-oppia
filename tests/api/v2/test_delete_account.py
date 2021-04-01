
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class DeleteAccountResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json']

    def setUp(self):
        super(DeleteAccountResourceTest, self).setUp()
        self.username = 'demo'
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user=user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'deleteaccount')
    
    def get_credentials(self):
        return self.create_apikey(username=self.username,
                                  api_key=self.api_key)
           
    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url))

    def test_deleted(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'password',
        }
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        # check return data
        response_data = self.deserialize(resp)
        self.assertTrue('message' in response_data)
        # check it doesn't contain the password
        self.assertFalse('password' in response_data)
        
        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start - 1, user_count_end)
        
    # invalid password
    def test_invalid_password(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'invalid',
        }
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)
        
    # no password
    def test_no_password(self):
        user_count_start = User.objects.all().count()
        data = {}
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)
        
    # invalid key
    def test_invalid_key(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'password',
        }
        
        credentials = self.create_apikey(username=self.username,
                                         api_key="1234")
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=credentials)
        self.assertHttpUnauthorized(resp)
        
        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)
        
    # already deleted account
    def test_already_deleted(self):
        user_count_start = User.objects.all().count()
        data = {
            'password': 'password',
        }
        
        # initial delete
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        
        user_count_mid = User.objects.all().count()
        self.assertEqual(user_count_start - 1, user_count_mid)
        
        # try deleting again
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpUnauthorized(resp)
        
        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start - 1, user_count_end)
    