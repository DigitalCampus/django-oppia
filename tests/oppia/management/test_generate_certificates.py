import os
import shutil

import pytest

from django.core import mail
from django.core.management import call_command
from django.forms import ValidationError
from django.conf import settings

from io import StringIO

from oppia.test import OppiaTestCase
from oppia.models import Award, CertificateTemplate

from profile.models import CustomField, UserProfileCustomField

from quiz.models import Quiz, Question, QuizAttempt, QuizAttemptResponse
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
                'tests/test_certificates.json',
                'tests/test_feedback.json',
                'tests/test_customfields.json',
                'tests/awards/test_feedback_display_name.json']

    TEST_IMG_NAMES = ['certificate_test2_aIeE1m6.png', 'certificate_test2_Aq5hcOr.png',
                      'certificate_portrait_valid_f1uzKEr.png', 'certificate_landscape_valid_XI8nTfU.png']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.copy_required_test_images(cls)

    def copy_required_test_images(cls):
        for test_img_name in cls.TEST_IMG_NAMES:
            src = os.path.join(settings.TEST_RESOURCES, 'certificate', 'templates', test_img_name)
            dst = os.path.join(settings.MEDIA_ROOT, 'certificate', 'templates', test_img_name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)

    def test_create_certificate_new(self):
        SettingProperties.set_bool(constants.OPPIA_EMAIL_CERTIFICATES, True)
        current_award = Award.objects.get(pk=4)
        self.assertTrue(current_award.certificate_pdf == "")
        self.assertEqual(len(mail.outbox), 0)

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.all().first()
        self.assertFalse(current_award.certificate_pdf == "")
        self.assertEqual(len(mail.outbox), 2)

    def test_create_certificate_all(self):

        current_award = Award.objects.all().first()
        self.assertTrue(current_award.certificate_pdf == "")
        self.assertEqual(len(mail.outbox), 0)

        call_command('generate_certificates', '--allcerts', stdout=StringIO())

        current_award = Award.objects.all().first()
        self.assertFalse(current_award.certificate_pdf == "")
        self.assertEqual(len(mail.outbox), 0)

    def test_create_certificate_no_data(self):
        ct = CertificateTemplate.objects.get(pk=4)
        ct.include_name = False
        ct.include_date = False
        ct.include_course_title = False
        ct.save()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())

    def test_create_certificate_validate_url(self):
        ct = CertificateTemplate.objects.get(pk=4)
        ct.validation = "URL"
        ct.save()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())

    def test_create_certificate_validate_qrcode(self):
        ct = CertificateTemplate.objects.get(pk=4)
        ct.validation = "QRCODE"
        ct.save()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())

    def test_email_certificates(self):
        SettingProperties.set_bool(constants.OPPIA_EMAIL_CERTIFICATES, True)
        call_command('generate_certificates', '--allcerts', stdout=StringIO())
        self.assertEqual(len(mail.outbox), 0)

    def test_email_certificates_one_time(self):
        SettingProperties.set_bool(constants.OPPIA_EMAIL_CERTIFICATES, True)
        call_command('generate_certificates', '--allcerts', stdout=StringIO())
        self.assertEqual(len(mail.outbox), 0)
        mail.outbox.clear()
        call_command('generate_certificates', '--allcerts', stdout=StringIO())
        self.assertEqual(len(mail.outbox), 0)

    #######
    # Display name tests
    #######
    def test_display_name_form_validation_registration_field(self):
        certificate_template = CertificateTemplate.objects.get(pk=1)
        certificate_template.display_name_method = \
            CertificateTemplate.DISPLAY_NAME_METHOD_REGISTRATION_FIELD
        certificate_template.feedback_field = None
        with self.assertRaises(ValidationError):
            certificate_template.save()

    def test_display_name_form_validation_feedback_field(self):
        certificate_template = CertificateTemplate.objects.get(pk=1)
        certificate_template.display_name_method = \
            CertificateTemplate.DISPLAY_NAME_METHOD_FEEDBACK_RESPONSE
        certificate_template.registration_form_field = None
        with self.assertRaises(ValidationError):
            certificate_template.save()

    def test_display_name_form_validation_invalid(self):
        certificate_template = CertificateTemplate.objects.get(pk=1)
        certificate_template.display_name_method = "RandomMethod"
        with self.assertRaises(ValidationError):
            certificate_template.save()

    # first/last name from profile
    def test_display_name_user_profile(self):
        certificate_template = CertificateTemplate.objects.get(pk=1)
        certificate_template.display_name_method = \
            CertificateTemplate.DISPLAY_NAME_METHOD_USER_FIRST_LAST
        certificate_template.save()

        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertEqual("demo user", display_name)
        self.assertTrue(valid)

        current_award = Award.objects.get(pk=4)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.get(pk=4)
        self.assertFalse(current_award.certificate_pdf == "")

    # registration form
    def test_display_name_reg_form_complete(self):

        cf = CustomField.objects.get(pk="country")
        certificate_template = CertificateTemplate.objects.get(pk=1)
        certificate_template.display_name_method = \
            CertificateTemplate.DISPLAY_NAME_METHOD_REGISTRATION_FIELD
        certificate_template.registration_form_field = cf
        certificate_template.save()

        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertEqual("FI", display_name)
        self.assertTrue(valid)

        current_award = Award.objects.get(pk=4)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.get(pk=4)
        self.assertFalse(current_award.certificate_pdf == "")

    def test_display_name_reg_form_incomplete(self):

        cf = CustomField.objects.get(pk="country")
        UserProfileCustomField.objects.all().delete()
        certificate_template = CertificateTemplate.objects.get(pk=3)
        certificate_template.display_name_method = \
            CertificateTemplate.DISPLAY_NAME_METHOD_REGISTRATION_FIELD
        certificate_template.registration_form_field = cf
        certificate_template.save()

        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertEqual(None, display_name)
        self.assertFalse(valid)

        current_award = Award.objects.get(pk=4)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.get(pk=4)
        self.assertTrue(current_award.certificate_pdf == "")

    def test_display_name_reg_form_changed(self):

        cf = CustomField.objects.get(pk="country")
        certificate_template = CertificateTemplate.objects.get(pk=1)
        certificate_template.display_name_method = \
            CertificateTemplate.DISPLAY_NAME_METHOD_REGISTRATION_FIELD
        certificate_template.registration_form_field = cf
        certificate_template.save()

        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertEqual("FI", display_name)
        self.assertTrue(valid)

        upcf = UserProfileCustomField.objects.get(key_name=cf,
                                                  user=self.normal_user)
        upcf.value_str = "This is my real name"
        upcf.save()

        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertEqual("This is my real name", display_name)
        self.assertTrue(valid)

    # feedback field
    def test_display_name_feedback_once(self):
        certificate_template = CertificateTemplate.objects.get(pk=5)
        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertEqual("my real name", display_name)
        self.assertTrue(valid)

        current_award = Award.objects.get(pk=10)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.get(pk=10)
        self.assertFalse(current_award.certificate_pdf == "")

    def test_display_name_feedback_none(self):
        QuizAttempt.objects.all().delete()
        certificate_template = CertificateTemplate.objects.get(pk=5)
        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertFalse(valid)

        current_award = Award.objects.get(pk=10)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.get(pk=10)
        self.assertTrue(current_award.certificate_pdf == "")

    def test_display_name_feedback_many(self):
        # add a new quiz attempt
        quiz = Quiz.objects.get(pk=41)
        question = Question.objects.get(pk=482)
        quiz_attempt = QuizAttempt(user=self.normal_user,
                                   quiz=quiz,
                                   score=0,
                                   maxscore=0)
        quiz_attempt.save()

        qa_response = QuizAttemptResponse(quizattempt=quiz_attempt,
                                          question=question,
                                          score=0,
                                          text="my new name")
        qa_response.save()

        certificate_template = CertificateTemplate.objects.get(pk=5)
        valid, display_name = certificate_template.display_name(
            self.normal_user)
        self.assertEqual("my new name", display_name)
        self.assertTrue(valid)

        current_award = Award.objects.get(pk=10)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.get(pk=10)
        self.assertFalse(current_award.certificate_pdf == "")

    ######
    # Resending certificates for users
    ######

    # valid user
    def test_resend_valid_user(self):
        SettingProperties.set_bool(constants.OPPIA_EMAIL_CERTIFICATES, True)
        current_award = Award.objects.get(pk=4)
        self.assertTrue(current_award.certificate_pdf == "")

        call_command('generate_certificates', stdout=StringIO())

        current_award = Award.objects.get(pk=4)
        self.assertFalse(current_award.certificate_pdf == "")
        original_pdf_name = current_award.certificate_pdf

        self.assertEqual(len(mail.outbox), 2)

        call_command('generate_certificates', '--user=2', stdout=StringIO())
        current_award = Award.objects.get(pk=4)
        new_pdf_name = current_award.certificate_pdf

        self.assertEqual(len(mail.outbox), 6)
        self.assertNotEqual(original_pdf_name, new_pdf_name)
        for email in mail.outbox:
            self.assertEqual("demo@me.com", email.to[0])

    # invalid user
    def test_resend_invalid_user(self):
        out = StringIO()
        call_command('generate_certificates', '--user=999', stdout=out)
        self.assertEqual(u'Invalid user id\n', out.getvalue())
