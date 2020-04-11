from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from settings import constants
from settings.models import SettingProperties

from tests.utils import get_api_url


class RegisterResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json']

    def setUp(self):
        super(RegisterResourceTest, self).setUp()
        self.url = get_api_url('v2', 'register')

    # check get method not allowed
    def test_get_list_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url,
                                                            format='json'))

    # check posting with no username
    def test_post_no_username(self):
        data = {
            'password': 'secret',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # check posting with no password
    def test_post_no_password(self):
        data = {
            'username': 'demo2',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # check posting with no email
    def test_post_no_email(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

    # check posting with invalid email
    def test_post_invalid_email(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'thisisnotanemailaddress',
            'passwordagain': 'secret',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # check posting with no passwordagain
    def test_post_no_passwordagain(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test no firstname
    def test_post_no_firstname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test firstname long enough
    def test_post_firstname_length(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'd',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test no lastname
    def test_post_no_lastname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test password long enough
    def test_post_password_length(self):
        data = {
            'username': 'demo2',
            'password': 's',
            'passwordagain': 's',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test password and password again not matching
    def test_post_password_match(self):
        data = {
            'username': 'demo2',
            'password': 's',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test lastname not long enough
    def test_post_lastname_length(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'u',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test created (all data valid)
    def test_post_created(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

    # test username already in use
    def test_username_in_use(self):
        data = {
            'username': 'demo',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    # test email address already in use
    def test_email_in_use(self):
        data = {
            'username': 'demo3',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@me.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

    def test_self_registration_disabled_cant_view(self):
        # turn off self registration
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                                   False)
        data = {
            'username': 'demo3',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo3@me.com',
            'first_name': 'demo',
            'last_name': 'user',
        }
        response = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(response)
        self.assertValidJSON(response.content)

        # turn back on
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                                   True)
