import pytest

from django.core.management import call_command
from django.core.management.base import CommandError

from io import StringIO

from oppia.models import Activity
from oppia.test import OppiaTestCase

from quiz.models import Quiz


class RegenerateCourseStructureTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_settings.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    def test_missing_course_shortname(self):
        with self.assertRaises(CommandError):
            call_command('regenerate_course_structure', stdout=StringIO())

    def test_course_fix_run(self):
        act_count_start = Activity.objects.all().count()
        quiz_count_start = Quiz.objects.all().count()

        call_command('regenerate_course_structure',
                     'ncd1-et',
                     stdout=StringIO())

        act_count_end = Activity.objects.all().count()
        quiz_count_end = Quiz.objects.all().count()

        self.assertEqual(act_count_start, act_count_end)
        # 8 quizzes added as not included in the original fixtures
        self.assertEqual(quiz_count_start+8, quiz_count_end)
