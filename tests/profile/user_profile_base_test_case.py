from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class UserProfileBaseTestCase(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json']

    @classmethod
    def setUpClass(cls):
        super(UserProfileBaseTestCase, cls).setUpClass()
        cls.username = 'demo'
        cls.user = User.objects.get(username=cls.username)
        cls.api_key = get_api_key(user=cls.user).key
        cls.base_data = {
            'email': 'demo@me.com',
            'first_name': 'demo',
            'last_name': 'user'
        }
        cls.url = get_api_url('v2', 'profileupdate')

    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)
