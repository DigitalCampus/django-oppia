import pytest

from django.core.management import call_command

from io import StringIO

from oppia.test import OppiaTestCase


class CleanCertificatesTest(OppiaTestCase):

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

    def test_clean_certs(self):
        call_command('clean_certificates', stdout=StringIO())
