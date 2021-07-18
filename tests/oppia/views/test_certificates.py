from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from oppia.models import CertificateTemplate
from oppia.test import OppiaTestCase


class CertificateViewTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'default_badges.json',
                'tests/awards/award-course.json',
                'tests/test_certificate_validation.json'
                ]

    STR_URL_VALIDATE = "oppia:certificate_validate"
    STR_VALID_TEMPLATE = "oppia/certificates/valid.html"
    STR_INVALID_TEMPLATE = "oppia/certificates/invalid.html"

    def test_certificate_valid_logged_in(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(
            reverse(self.STR_URL_VALIDATE,
                    args=["81477a43-6098-4d0a-bcfb-4979e0b4036b"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.STR_VALID_TEMPLATE)

    def test_certificate_valid_notlogged_in(self):
        response = self.client.get(
            reverse(self.STR_URL_VALIDATE,
                    args=["81477a43-6098-4d0a-bcfb-4979e0b4036b"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.STR_VALID_TEMPLATE)

    def test_certificate_invalid_logged_in(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(
            reverse(self.STR_URL_VALIDATE,
                    args=["12345678-1234-1234-1234-123456789abc"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.STR_INVALID_TEMPLATE)

    def test_certificate_invalid_not_logged_in(self):
        response = self.client.get(reverse(self.STR_URL_VALIDATE,
                                           args=["1234"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.STR_INVALID_TEMPLATE)

    def test_certificate_no_uuid(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse(self.STR_URL_VALIDATE,
                                    args=[""]))

    def test_certificate_not_a_uuid(self):
        response = self.client.get(reverse(self.STR_URL_VALIDATE,
                                           args=["9999999999"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.STR_INVALID_TEMPLATE)
