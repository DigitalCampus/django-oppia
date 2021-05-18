
# AwardsResource
from django.contrib.auth.models import User
from oppia.test import OppiaTestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class AwardsResourceTest(ResourceTestCaseMixin, OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_course_permissions.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json',
                'tests/test_awardcourse.json']

    def setUp(self):
        super(AwardsResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        api_key = get_api_key(user=user)
        self.auth_data = {
            'username': 'demo',
            'api_key': api_key.key,
        }
        self.url = get_api_url('v2', 'awards')

    # check post not allowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url,
                                                             format='json',
                                                             data={}))

    # check unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'demo',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url,
                                                        format='json',
                                                        data=data))

    # check authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url,
                                   format='json',
                                   data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        award = self.deserialize(resp)['objects'][0]
        self.assertTrue('certificate_pdf' in award)
        self.assertTrue('award_date' in award)
        self.assertTrue('badge_icon' in award)
        self.assertTrue('description' in award)

    # check returning a set of objects - expecting zero
    def test_no_objects(self):
        user = User.objects.get(username='admin')
        api_key = get_api_key(user=user)
        self.auth_data = {
            'username': 'admin',
            'api_key': api_key.key,
        }
        self.url = get_api_url('v2', 'awards')
        resp = self.api_client.get(self.url,
                                   format='json',
                                   data=self.auth_data)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
