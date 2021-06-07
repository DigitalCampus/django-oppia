from django.urls import reverse

from oppia.models import CertificateTemplate
from oppia.test import OppiaTestCase


class CertificateViewTest(OppiaTestCase):
    
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_certificate_validation.json'
                'default_badges.json']

    STR_URL_VALIDATE = "oppia:certificate_validate"
    STR_VALID_TEMPLATE = "oppia/certificates/valid.html"
    STR_INVALID_TEMPLATE = "oppia/certificates/invalid.html"

    def test_certificate_valid_logged_in(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(reverse(STR_URL_VALIDATE,
                                           args=["1234"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.STR_VALID_TEMPLATE)

    def test_certificate_valid_notlogged_in(self):
        response = self.client.get(reverse(STR_URL_VALIDATE,
                                           args=["1234"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.STR_VALID_TEMPLATE)

    def test_certificate_invalid_logged_in(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(reverse(STR_URL_VALIDATE,
                                           args=["1234"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.STR_INVALID_TEMPLATE)

    def test_certificate_invalid_not_logged_in(self):
        response = self.client.get(reverse(STR_URL_VALIDATE,
                                           args=["1234"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.STR_INVALID_TEMPLATE)

    def test_certificate_no_guid(self):
        response = self.client.get(reverse(STR_URL_VALIDATE,
                                           args=[""]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.STR_INVALID_TEMPLATE)

    def test_certificate_not_a_guid(self):
        response = self.client.get(reverse(STR_URL_VALIDATE,
                                           args=["9999999999"]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.STR_INVALID_TEMPLATE)
