from django.conf import settings
from oppia.test import OppiaTestCase


class ImplementationCoreTest(OppiaTestCase):

    def test_settings(self):
        self.assertEqual(settings.OPPIA_ALLOW_SELF_REGISTRATION, True)
        self.assertEqual(settings.OPPIA_SHOW_GRAVATARS, True)
        self.assertEqual(settings.OPPIA_STAFF_ONLY_UPLOAD, True)

    def test_theme(self):
        with open("./static/css/oppia.scss", 'r') as oppia_scss:
            css_file = oppia_scss.read().replace("\n", "")

        self.assertNotEqual(css_file.find('$oppia-lighter: #c1e552;'), -1)
        self.assertNotEqual(css_file.find('$oppia-light: #9aca3c;'), - 1)
        self.assertNotEqual(css_file.find('$oppia-mid: #689e3a;'), -1)
        self.assertNotEqual(css_file.find('$oppia-dark: #628817;'), -1)
