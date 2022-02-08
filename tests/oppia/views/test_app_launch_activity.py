
from django.urls import reverse
from oppia.test import OppiaTestCase
from django.http import Http404

from tests.utils import update_course_visibility


class AppLaunchActivityTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    STR_LAUNCHER_TEMPLATE = 'course/app_launcher.html'
    STR_URL_REDIRECT = 'oppia:app_launch_activity_redirect'
    valid_digest = '11cc12291f730160c324b727dd2268b612137'
    invalid_digest = '1ab2c3d4e5f6'
    valid_course = 'anc1-all'
    invalid_course = 'mycourse'

    # all users should be able to access without logging in
    def test_access_valid_digest(self):
        url = ('%s?digest=' + self.valid_digest) \
            % reverse(self.STR_URL_REDIRECT)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.STR_LAUNCHER_TEMPLATE)
        self.assertEqual(200, response.status_code)

    def test_access_no_digest(self):
        url = reverse(self.STR_URL_REDIRECT)
        response = self.client.get(url)
        self.assertRaises(ValueError)
        self.assertTemplateUsed(response, self.STR_LAUNCHER_TEMPLATE)
        self.assertEqual(200, response.status_code)

    def test_access_invalid_digest(self):
        url = ('%s?digest=' + self.invalid_digest) \
            % reverse(self.STR_URL_REDIRECT)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.STR_LAUNCHER_TEMPLATE)
        self.assertEqual(200, response.status_code)

    def test_access_valid_course(self):
        url = ('%s?course=' + self.valid_course) \
            % reverse(self.STR_URL_REDIRECT)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.STR_LAUNCHER_TEMPLATE)
        self.assertEqual(200, response.status_code)

    def test_access_invalid_course(self):
        url = ('%s?course=' + self.invalid_course) \
            % reverse(self.STR_URL_REDIRECT)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.STR_LAUNCHER_TEMPLATE)
        self.assertEqual(200, response.status_code)

    def test_no_access_for_draft_course(self):
        url = ('%s?course=' + self.valid_course) \
            % reverse(self.STR_URL_REDIRECT)
        update_course_visibility(1, False, True)
        response = self.client.get(url)
        self.assertRaises(Http404)
        self.assertTemplateUsed(response, self.STR_LAUNCHER_TEMPLATE)
        self.assertEqual(200, response.status_code)
        update_course_visibility(1, False, False)
