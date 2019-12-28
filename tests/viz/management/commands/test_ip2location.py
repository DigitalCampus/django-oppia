
from django.core.management import call_command
from io import StringIO
from oppia.test import OppiaTestCase


class Ip2LocationTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json']

    def test_ip2location_output(self):
        out = StringIO()
        call_command('ip2location', stdout=out)
        self.assertEqual(u'completed', out.getvalue()[0:9])
