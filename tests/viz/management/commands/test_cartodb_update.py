from io import StringIO
from django.core.management import call_command
from oppia.test import OppiaTestCase


class CartoDBUpdateTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    def test_cartodb_output(self):
        out = StringIO()
        call_command('cartodb_update', stdout=out)
        # API KEY won't be valid
        self.assertEqual(u'Please check', out.getvalue()[0:12])
