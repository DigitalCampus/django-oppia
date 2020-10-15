import pytest

from django.core.management import call_command
from io import StringIO
from oppia.test import OppiaTransactionTestCase
from viz.models import UserLocationVisualization


class Ip2LocationTest(OppiaTransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_ip2location.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_ip2location_output(self):

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        # @TODO - replace with old_count+2 once mock server set up
        self.assertEqual(old_count, new_count)
