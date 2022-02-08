from django.core.management import call_command
from django.core.management.base import CommandError

from io import StringIO

from oppia.models import Tracker
from oppia.test import OppiaTestCase

from quiz.models import QuizAttempt

from settings import constants
from settings.models import SettingProperties


class PopulateCourseVersionTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_settings.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_course_permissions.json']

    def test_update_courseversion(self):
        out = StringIO()
        count_start = Tracker.objects.filter(
            course_version__isnull=True).count()
        call_command('populate_courseversion', stdout=out)
        count_end = Tracker.objects.filter(course_version__isnull=True).count()
        self.assertEqual(count_start-1, count_end)

    def test_update_courseversion_no_more_trackers(self):
        out = StringIO()
        count_start = Tracker.objects.filter(
            course_version__isnull=True).count()
        call_command('populate_courseversion', stdout=out)
        # re-run command to check
        call_command('populate_courseversion', stdout=out)
        count_end = Tracker.objects.filter(course_version__isnull=True).count()
        self.assertEqual(count_start-1, count_end)
