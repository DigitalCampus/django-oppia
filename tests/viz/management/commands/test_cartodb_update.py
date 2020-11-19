from io import StringIO

import re
from django.core.management import call_command
from oppia.test import OppiaTestCase
from settings import constants
from settings.models import SettingProperties


class CartoDBUpdateTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    cartodb_valid_response = './oppia/fixtures/tests/ipstack/200_valid.json'
    cartodb_uri_regex = re.compile("https?://(w+).cartodb.com/api/v2/sql??(?:&?[^=&]*=[^=&]*)*")

    def test_cartodb_output(self):
        SettingProperties.set_string(constants.OPPIA_CARTODB_ACCOUNT, "digital-campus")
        SettingProperties.set_string(constants.OPPIA_CARTODB_KEY, "7724a72cc5bb846b8cf02806c0112a5f7ef75b30")
        SettingProperties.set_string(constants.OPPIA_HOSTNAME, "https://demo.oppia-mobile.org/")

        out = StringIO()
        call_command('cartodb_update', stdout=out)
        # API KEY won't be valid
        self.assertEqual(u'Please check', out.getvalue()[0:12])
