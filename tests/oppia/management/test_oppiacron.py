import pytest

from io import StringIO
from django.core.management import call_command
from oppia.test import OppiaTestCase


class OppiaCronTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    @pytest.mark.xfail(reason="works on local, but not on Github workflow \
        see issue: https://oppia.atlassian.net/browse/OPPIA-19")
    def test_oppiacron_output(self):
        out = StringIO()
        call_command('oppiacron', stdout=out)
        self.assertEqual(u'Cleaning up:', out.getvalue()[0:12])

    @pytest.mark.xfail(reason="works on local, but not on Github workflow \
        see issue: https://oppia.atlassian.net/browse/OPPIA-19")
    def test_oppiacron_hours_output(self):
        out = StringIO()
        call_command('oppiacron', '--hours=48', stdout=out)
        self.assertEqual(u'Cleaning up:', out.getvalue()[0:12])
