import os

import httpretty
import re

from django.conf import settings
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

    ipstack_path = os.path.join(settings.FIXTURES_PATH, 'tests', 'ipstack')
    ipstack_valid_response = os.path.join(ipstack_path, '200_valid.json' )
    ipstack_valid_response_no_city = os.path.join(ipstack_path, '200_valid_no_city.json')
    ipstack_valid_response_no_region = os.path.join(ipstack_path, '200_valid_no_region.json')
    ipstack_valid_response_no_city_region = os.path.join(ipstack_path, '200_valid_no_city_region.json')
    ipstack_valid_response_lat_lng_0 = os.path.join(ipstack_path, '200_valid_lat_lng_0.json')
    ipstack_uri_regex = \
        re.compile("https?://api.ipstack.com/??(?:&?[^=&]*=[^=&]*)*")

    @httpretty.activate
    def test_ip2location_output(self):

        ipstack_response = get_file_contents(self.ipstack_valid_response)
        httpretty.register_uri(httpretty.GET,
                               self.ipstack_uri_regex,
                               body=ipstack_response)

        SettingProperties.set_string(constants.OPPIA_IPSTACK_APIKEY,
                                     "FAKE_APIKEY")

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        self.assertEqual(old_count+2, new_count)

    @httpretty.activate
    def test_ip2location_no_city(self):

        ipstack_response = get_file_contents(
            self.ipstack_valid_response_no_city)
        httpretty.register_uri(httpretty.GET,
                               self.ipstack_uri_regex,
                               body=ipstack_response)

        SettingProperties.set_string(constants.OPPIA_IPSTACK_APIKEY,
                                     "FAKE_APIKEY")

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        self.assertEqual(old_count+2, new_count)

    @httpretty.activate
    def test_ip2location_no_region(self):

        ipstack_response = get_file_contents(
            self.ipstack_valid_response_no_region)
        httpretty.register_uri(httpretty.GET,
                               self.ipstack_uri_regex,
                               body=ipstack_response)

        SettingProperties.set_string(constants.OPPIA_IPSTACK_APIKEY,
                                     "FAKE_APIKEY")

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        self.assertEqual(old_count+2, new_count)

    @httpretty.activate
    def test_ip2location_no_city_region(self):

        ipstack_response = get_file_contents(
            self.ipstack_valid_response_no_city_region)
        httpretty.register_uri(httpretty.GET,
                               self.ipstack_uri_regex,
                               body=ipstack_response)

        SettingProperties.set_string(constants.OPPIA_IPSTACK_APIKEY,
                                     "FAKE_APIKEY")

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        self.assertEqual(old_count+2, new_count)

    @httpretty.activate
    def test_ip2location_lat_lng_0(self):

        ipstack_response = get_file_contents(
            self.ipstack_valid_response_lat_lng_0)
        httpretty.register_uri(httpretty.GET,
                               self.ipstack_uri_regex,
                               body=ipstack_response)

        SettingProperties.set_string(constants.OPPIA_IPSTACK_APIKEY,
                                     "FAKE_APIKEY")

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        self.assertEqual(old_count, new_count)

    @httpretty.activate
    def test_ip2location_no_key(self):

        ipstack_response = get_file_contents(
            self.ipstack_valid_response_lat_lng_0)
        httpretty.register_uri(httpretty.GET,
                               self.ipstack_uri_regex,
                               body=ipstack_response)

        SettingProperties.set_string(constants.OPPIA_IPSTACK_APIKEY, "")

        old_count = UserLocationVisualization.objects.all().count()
        call_command('ip2location', stdout=StringIO())

        self.assertRaises(UserLocationVisualization.DoesNotExist)

        new_count = UserLocationVisualization.objects.all().count()

        self.assertEqual(old_count, new_count)
