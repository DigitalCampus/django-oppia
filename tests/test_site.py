# oppia/tests/test_site.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from tests.utils import *

class BasicTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get(reverse('oppia_home'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('profile_register'), {'username': 'demo', 'password': 'secret', 'password_again': 'secret', 'email': 'demo@demo.com', 'first_name': 'demo', 'last_name': 'user'})
        self.assertEqual(response.status_code, 302)

    def test_register_with_no_data(self):
        response = self.client.post(reverse('profile_register'), {})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('profile_login'), {'username': 'demo', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)

    # TODO test login redirected correctly for all pages
    # except those with login exempt
