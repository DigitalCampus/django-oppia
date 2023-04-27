
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class UserCohortsResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_cohorts.json']

    def setUp(self):
        super(UserCohortsResourceTest, self).setUp()
        self.user = User.objects.get(username='demo')
        self.admin = User.objects.get(username='admin')
        self.staff = User.objects.get(username='staff')
        self.teacher = User.objects.get(username='teacher')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=self.user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=self.admin).key
        }
        self.staff_auth = {
            'username': 'staff',
            'api_key': get_api_key(user=self.staff).key
        }
        self.teacher_auth = {
            'username': 'teacher',
            'api_key': get_api_key(user=self.teacher).key
        }

        self.url = get_api_url('v2', 'cohorts')

    def assert_valid_response_and_get_list(self, resp):
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        return self.deserialize(resp)

    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))

    def test_user_with_no_cohorts(self):
        resp = self.api_client.get(self.url, format='json', data=self.admin_auth)
        cohorts = self.assert_valid_response_and_get_list(resp)

        self.assertEqual(len(cohorts), 0)

    def test_user_with_cohorts(self):
        resp = self.api_client.get(self.url, format='json', data=self.user_auth)
        cohorts = self.assert_valid_response_and_get_list(resp)
        self.assertEqual(len(cohorts), 2)
        self.assertEqual(1, cohorts[0])
        self.assertEqual(2, cohorts[1])

    # Test that if a user belongs more than once to a cohort (multiple roles), they are not duplicated
    def test_no_duplicate_cohorts(self):
        resp = self.api_client.get(self.url, format='json', data=self.teacher_auth)
        cohorts = self.assert_valid_response_and_get_list(resp)
        self.assertEqual(len(cohorts), 1)

    def test_cohorts_returned_after_login(self):
        url = get_api_url('v2', 'user')
        data = {
            'username': 'demo',
            'password': 'password'
        }
        resp = self.api_client.post(url, format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        # check return data
        response_data = self.deserialize(resp)
        self.assertTrue('cohorts' in response_data)
        self.assertEqual(len(response_data['cohorts']), 2)
        self.assertEqual(1, response_data['cohorts'][0])
        self.assertEqual(2, response_data['cohorts'][1])
