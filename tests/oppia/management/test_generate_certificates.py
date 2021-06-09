import pytest

from django.core import mail
from django.core.management import call_command

from io import StringIO

from oppia.test import OppiaTestCase
from oppia.models import Award, CertificateTemplate

from settings import constants
from settings.models import SettingProperties


class GenerateCertificatesTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json',
                'tests/awards/award-course.json',
                'tests/test_certificatetemplate.json',
                'tests/test_certificates.json']

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_create_certificate_new(self):

        current_award = Award.objects.get(pk=4)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.all().first()
        self.assertFalse(current_award.certificate_pdf == "")

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_create_certificate_all(self):

        current_award = Award.objects.all().first()
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', '--allcerts', stdout=StringIO())

        current_award = Award.objects.all().first()
        self.assertFalse(current_award.certificate_pdf == "")

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_create_certificate_no_data(self):
        ct = CertificateTemplate.objects.get(pk=4)
        ct.include_name = False
        ct.include_date = False
        ct.include_course_title = False
        ct.save()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_create_certificate_validate_url(self):
        ct = CertificateTemplate.objects.get(pk=4)
        ct.validation = "URL"
        ct.save()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_create_certificate_validate_qrcode(self):
        ct = CertificateTemplate.objects.get(pk=4)
        ct.validation = "QRCODE"
        ct.save()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())
        
    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_email_certificates(self):
        SettingProperties.set_bool(constants.OPPIA_EMAIL_CERTIFICATES, True)
        call_command('generate_certificates', '--allcerts', stdout=StringIO())
        self.assertEqual(len(mail.outbox), 3)

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_email_certificates_one_time(self):
        SettingProperties.set_bool(constants.OPPIA_EMAIL_CERTIFICATES, True)
        call_command('generate_certificates', '--allcerts', stdout=StringIO())
        self.assertEqual(len(mail.outbox), 3)
        mail.outbox.clear()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())
        self.assertEqual(len(mail.outbox), 0)
