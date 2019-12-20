from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class Ip2LocationTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json']
    
    def setUp(self):
        super(Ip2LocationTest, self).setUp()

    def test_ip2location_output(self):
        out = StringIO()
        call_command('ip2location', stdout=out)
        self.assertEqual(u'completed', out.getvalue()[0:9])