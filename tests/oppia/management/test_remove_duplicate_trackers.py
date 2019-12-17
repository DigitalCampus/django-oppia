
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

from oppia.models import Tracker


class RemoveDuplicateTrackersTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_permissions.json',
                'default_badges.json']

    def test_remove_no_duplicates(self):
        out = StringIO()
        tracker_count_start = Tracker.objects.all().count()

        call_command('remove_duplicate_trackers', stdout=out)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    '''
    def test_remove_with_duplicates(self):
        Tracker.objects.create(
            user_id=1,
            course_id = 1,
            type = "page",
            completed = True,
            time_taken = 280,
            activity_title = "{\"en\": \"Calculating the uptake of antenatal care services\"}",
            section_title = "{\"en\": \"Planning Antenatal Care\"}",
            uuid = "835713f3-b85e-4960-9cdf-128f04014178")
        out = StringIO()
        tracker_count_start = Tracker.objects.all().count()

        call_command('remove_duplicate_trackers', stdout=out)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start-1, tracker_count_end)
    '''

