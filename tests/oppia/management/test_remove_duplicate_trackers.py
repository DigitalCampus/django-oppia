import pytest
import unittest

from unittest import mock
from django.conf import settings
from django.core.management import call_command
from oppia.test import OppiaTestCase
from io import StringIO
from oppia.models import Tracker


class RemoveDuplicateTrackersTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    def test_remove_no_duplicates(self):
        out = StringIO()
        tracker_count_start = Tracker.objects.all().count()

        call_command('remove_duplicate_trackers', stdout=out)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @mock.patch("oppia.management.commands.remove_duplicate_trackers.input")
    def _call_wrapper(self, response_value, mock_input=None):
        def input_response(message):
            return response_value
        mock_input.side_effect = input_response
        out = StringIO()
        call_command('remove_duplicate_trackers', stdout=out)
        return out.getvalue().rstrip()

    @pytest.mark.xfail(reason="works on local, but not on Github workflow \
        see issue: https://github.com/DigitalCampus/django-oppia/issues/691")
    @unittest.skipIf(settings.DATABASES['default']['ENGINE']
                     == 'django.db.backends.sqlite3',
                     "This is an sqlite-specific issue")
    def test_remove_with_duplicates(self):
        Tracker.objects.create(
            user_id=1,
            course_id=1,
            type="page",
            completed=True,
            time_taken=280,
            activity_title="{\"en\":"
            "\"Calculating the uptake of antenatal care services\"}",
            section_title="{\"en\": \"Planning Antenatal Care\"}",
            uuid="835713f3-b85e-4960-9cdf-128f04014178")
        tracker_count_start = Tracker.objects.all().count()

        self._call_wrapper('y')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start-1, tracker_count_end)
