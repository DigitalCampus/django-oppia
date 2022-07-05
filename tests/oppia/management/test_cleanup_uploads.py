
from io import StringIO
from django.core.management import call_command
from oppia.test import OppiaTestCase


class CleanUpUploadsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_course_statuses.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def test_cleanup_uploads(self):
        out = StringIO()
        call_command('cleanup_uploads', stdout=out)
