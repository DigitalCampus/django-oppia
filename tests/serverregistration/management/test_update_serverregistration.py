import datetime
import os
import re
import httpretty

from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from oppia.test import OppiaTestCase
from settings import constants
from settings.models import SettingProperties
from tests.utils import get_file_contents


class ServerRegistrationUpdateTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json',
                'tests/test_viz.json']

    imp_site_url = "https://implementations.oppia-mobile.org"
    implementations_path = os.path.join(settings.FIXTURES_PATH, 'tests', 'implementations')
    update_valid_response = os.path.join(implementations_path, '201_created.json')
    get_api_key_valid_response = os.path.join(implementations_path, 'api_key_created.json')
    update_uri_regex = re.compile(
        imp_site_url + "/api/oppia/?(?:&?[^=&]*=[^=&]*)*")
    get_api_key_uri_regex = re.compile(
        imp_site_url + "/get-api-key/?(?:&?[^=&]*=[^=&]*)*")

    STR_COMMAND = 'update_server_registration'

    @httpretty.activate
    def test_update_server_registered(self):
        api_key_response = get_file_contents(self.get_api_key_valid_response)
        httpretty.register_uri(httpretty.GET,
                               self.get_api_key_uri_regex,
                               body=api_key_response)
        update_response = get_file_contents(self.update_valid_response)
        httpretty.register_uri(httpretty.POST,
                               self.update_uri_regex,
                               body=update_response)

        SettingProperties.set_bool(constants.OPPIA_SERVER_REGISTERED, True)
        SettingProperties.set_bool(constants.OPPIA_SERVER_REGISTER_EMAIL_NOTIF,
                                   True)
        SettingProperties.set_bool(constants.OPPIA_SERVER_REGISTER_NO_COURSES,
                                   True)
        SettingProperties.set_bool(constants.OPPIA_SERVER_REGISTER_NO_USERS,
                                   True)
        out = StringIO()
        call_command(self.STR_COMMAND, stdout=out)

        # check api key matches the one returned
        api_key = SettingProperties.get_property(
            constants.OPPIA_SERVER_REGISTER_APIKEY, '')
        self.assertEqual('AwZfRgB.rxpVnadfn8K6sgY8qYOp8', api_key)

    @httpretty.activate
    def test_update_server_unregistered(self):
        api_key_response = get_file_contents(self.get_api_key_valid_response)
        httpretty.register_uri(httpretty.GET,
                               self.get_api_key_uri_regex,
                               body=api_key_response)
        update_response = get_file_contents(self.update_valid_response)
        httpretty.register_uri(httpretty.POST,
                               self.update_uri_regex,
                               body=update_response)
        out = StringIO()
        call_command(self.STR_COMMAND, stdout=out)

        # check api key matches the one returned
        api_key = SettingProperties.get_property(
            constants.OPPIA_SERVER_REGISTER_APIKEY, '')
        self.assertEqual('', api_key)

    @httpretty.activate
    def test_update_server_last_updated(self):
        api_key_response = get_file_contents(self.get_api_key_valid_response)
        httpretty.register_uri(httpretty.GET,
                               self.get_api_key_uri_regex,
                               body=api_key_response)
        update_response = get_file_contents(self.update_valid_response)
        httpretty.register_uri(httpretty.POST,
                               self.update_uri_regex,
                               body=update_response)
        SettingProperties.set_bool(constants.OPPIA_SERVER_REGISTERED, True)
        SettingProperties.set_string(constants.OPPIA_SERVER_REGISTER_LAST_SENT,
                                     timezone.now())
        out = StringIO()
        call_command(self.STR_COMMAND, stdout=out)

    @httpretty.activate
    def test_update_server_last_over_week_ago(self):
        api_key_response = get_file_contents(self.get_api_key_valid_response)
        httpretty.register_uri(httpretty.GET,
                               self.get_api_key_uri_regex,
                               body=api_key_response)
        update_response = get_file_contents(self.update_valid_response)
        httpretty.register_uri(httpretty.POST,
                               self.update_uri_regex,
                               body=update_response)
        SettingProperties.set_bool(constants.OPPIA_SERVER_REGISTERED, True)

        last_sent = timezone.now() - datetime.timedelta(days=10)

        SettingProperties.set_string(constants.OPPIA_SERVER_REGISTER_LAST_SENT,
                                     last_sent)
        out = StringIO()
        call_command(self.STR_COMMAND, stdout=out)
