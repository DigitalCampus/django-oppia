import httpretty
import pytest
import re

from django.core.management import call_command
from io import StringIO

from settings import constants
from oppia.test import OppiaTransactionTestCase
from settings.models import SettingProperties
from tests.utils import get_file_contents
from viz.models import UserLocationVisualization


class Ip2LocationTest(OppiaTransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_ip2location.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    ipstack_valid_response = './oppia/fixtures/tests/ipstack/200_valid.json'
    ipstack_uri_regex = re.compile("https?://api.ipstack.com/??(?:&?[^=&]*=[^=&]*)*")

    @httpretty.activate
    def test_ip2location_output(self):

        ipstack_response = get_file_contents(self.ipstack_valid_response)
        httpretty.register_uri( httpretty.GET, self.ipstack_uri_regex, body=ipstack_response)

        SettingProperties.set_string(constants.OPPIA_IPSTACK_APIKEY, "FAKE_APIKEY")

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        self.assertEqual(old_count+2, new_count)
