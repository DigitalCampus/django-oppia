import pytest

from io import StringIO
from django.core.management import call_command
from oppia.test import OppiaTestCase


class OppiaCronTest(OppiaTestCase):

    @pytest.mark.xfail(reason="works on local, but not on Github workflow \
        see issue: https://github.com/DigitalCampus/django-oppia/issues/690")
    def test_oppiacron_output(self):
        out = StringIO()
        call_command('oppiacron', stdout=out)
        self.assertEqual(u'Cleaning up:', out.getvalue()[0:12])

    @pytest.mark.xfail(reason="works on local, but not on Github workflow \
        see issue: https://github.com/DigitalCampus/django-oppia/issues/690")
    def test_oppiacron_hours_output(self):
        out = StringIO()
        call_command('oppiacron', '--hours=48', stdout=out)
        self.assertEqual(u'Cleaning up:', out.getvalue()[0:12])
