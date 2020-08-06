
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class MediaResourceTest(ResourceTestCaseMixin, TransactionTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_av_uploadedmedia.json']

    def setUp(self):
        super(MediaResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        admin = User.objects.get(username='admin')
        staff = User.objects.get(username='staff')
        teacher = User.objects.get(username='teacher')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=admin).key
        }
        self.staff_auth = {
            'username': 'staff',
            'api_key': get_api_key(user=staff).key
        }
        self.teacher_auth = {
            'username': 'teacher',
            'api_key': get_api_key(user=teacher).key
        }
        self.url = get_api_url('v2', 'media')

    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.post(self.url, format='json', data={}))

        # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'demo',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(
            self.api_client.get(self.url, format='json', data=data))

    # test authorized
    def test_authorized(self):
        resp = self.api_client.get(
            self.url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)

    # test get with valid medai md5
    def test_existing_media(self):
        url = self.url + "md5/33e2c3cfc3e91d06b8a826f626fe39c3"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        response_data = self.deserialize(response)
        self.assertEqual('33e2c3cfc3e91d06b8a826f626fe39c3',
                         response_data['digest'])
        self.assertEqual(82, response_data['length'])
        self.assertEqual('ldrshp-mgmt-unit-2-risk-mgmt-D-v2.m4v',
                         response_data['filename'])
        self.assertEqual('http://testserver/media/uploaded/2018/02/' +
                         'ldrshp-mgmt-unit-2-risk-mgmt-D-v2.m4v',
                         response_data['download_url'])
        self.assertEqual(0,
                         response_data['filesize'])

    # test get with md5 that doesn;t exist
    def test_media_not_uploaded(self):
        url = self.url + "md5/aaaaaaaaaa"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertEqual(404, response.status_code)
