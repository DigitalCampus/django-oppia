import os

from django.core.management import call_command
from django.core.management.base import CommandError
from django.conf import settings

from io import StringIO

from oppia.models import Tracker
from oppia.test import OppiaTestCase

from quiz.models import QuizAttempt


class ActivityLogsFromFolderTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_settings.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    activity_logs_folder = os.path.join(settings.TEST_RESOURCES, 'activity_logs')

    def test_no_folder(self):
        out = StringIO()
        count_start = Tracker.objects.all().count()
        with self.assertRaises(CommandError):
            call_command('activitylogs_fromfolder', stdout=out)
        count_end = Tracker.objects.all().count()
        self.assertEqual(count_start, count_end)

    def test_invalid_folder(self):
        out = StringIO()
        count_start = Tracker.objects.all().count()
        with self.assertRaises(SystemExit):
            call_command('activitylogs_fromfolder',
                         os.path.join(self.activity_logs_folder, 'folder-does-not_exist'),
                         stdout=out)
        count_end = Tracker.objects.all().count()
        self.assertEqual(count_start, count_end)

    # not a directory
    def test_not_a_folder(self):
        out = StringIO()
        count_start = Tracker.objects.all().count()
        with self.assertRaises(SystemExit):
            call_command('activitylogs_fromfolder',
                         os.path.join(self.activity_logs_folder, 'basic_activity.json'),
                         stdout=out)
        count_end = Tracker.objects.all().count()
        self.assertEqual(count_start, count_end)

    # no json files
    def test_no_json_files(self):
        out = StringIO()
        count_start = Tracker.objects.all().count()
        with self.assertRaises(SystemExit):
            call_command('activitylogs_fromfolder',
                         os.path.join(self.activity_logs_folder, 'no_json_files'),
                         stdout=out)
        count_end = Tracker.objects.all().count()
        self.assertEqual(count_start, count_end)

    def test_folder(self):
        out = StringIO()
        tracker_count_start = Tracker.objects.all().count()
        qa_count_start = QuizAttempt.objects.all().count()

        call_command('activitylogs_fromfolder',
                     self.activity_logs_folder,
                     stdout=out)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        qa_count_end = QuizAttempt.objects.all().count()
        self.assertEqual(qa_count_start+1, qa_count_end)
