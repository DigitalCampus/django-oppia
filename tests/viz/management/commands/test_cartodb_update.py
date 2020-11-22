from io import StringIO

import re

import httpretty
from django.core.management import call_command
from oppia.test import OppiaTestCase
from settings import constants
from settings.models import SettingProperties
from tests.utils import get_file_contents


class CartoDBUpdateTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json',
                'tests/test_viz.json']

    cartodb_valid_response = './oppia/fixtures/tests/cartodb/200_valid.json'
    cartodb_uri_regex = re.compile(
        "https://[A-Za-z0-9-]+.cartodb.com/api/v2/sql??(?:&?[^=&]*=[^=&]*)*")


    @httpretty.activate
    def test_cartodb_output(self):
        cartodb_response = get_file_contents(self.cartodb_valid_response)
        httpretty.register_uri(httpretty.GET,
                               self.cartodb_uri_regex,
                               body=cartodb_response)

        SettingProperties.set_string(constants.OPPIA_CARTODB_ACCOUNT,
                                     "account")
        SettingProperties.set_string(constants.OPPIA_CARTODB_KEY,
                                     "FAKE_APIKEY")
        SettingProperties.set_string(constants.OPPIA_HOSTNAME, "localhost")

        out = StringIO()
        call_command('cartodb_update', stdout=out)

    @httpretty.activate
    def test_cartodb_no_key_account(self):
        cartodb_response = get_file_contents(self.cartodb_valid_response)
        httpretty.register_uri(httpretty.GET,
                               self.cartodb_uri_regex,
                               body=cartodb_response)

        SettingProperties.set_string(constants.OPPIA_CARTODB_ACCOUNT, None)
        SettingProperties.set_string(constants.OPPIA_CARTODB_KEY, None)
        SettingProperties.set_string(constants.OPPIA_HOSTNAME, None)

        out = StringIO()
        call_command('cartodb_update', stdout=out)
