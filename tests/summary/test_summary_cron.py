from django.core.management import call_command

from io import StringIO

from oppia.test import OppiaTestCase
from oppia.models import Tracker, Points
from settings.models import SettingProperties
from summary.models import CourseDailyStats


class SummaryCronTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'default_badges.json',
                'tests/test_search_tracker.json',
                'tests/test_course_permissions.json']

    def test_summary_cron_open_cron_open(self):
        # check lock not set
        lock = SettingProperties.get_int('oppia_summary_cron_lock', 999)
        self.assertEqual(lock, 999)
        lock = SettingProperties.get_int('oppia_cron_lock', 999)
        self.assertEqual(lock, 999)

        call_command('update_summaries', stdout=StringIO())

        # check new details on pks
        tracker_id = SettingProperties.get_int('last_tracker_pk', 0)
        self.assertEqual(tracker_id, 1484221)
        # this id is from the test_tracker data

        # check unlocked again
        lock = SettingProperties.get_int('oppia_summary_cron_lock', 999)
        self.assertEqual(lock, 999)

    def test_summary_cron_locked_cron_open(self):
        # set locked
        SettingProperties.set_int('oppia_summary_cron_lock', 1)
        lock = SettingProperties.get_int('oppia_summary_cron_lock', 0)
        self.assertEqual(lock, 1)

        lock = SettingProperties.get_int('oppia_cron_lock', 999)
        self.assertEqual(lock, 999)

        call_command('update_summaries', stdout=StringIO())

        # check new details on pks
        # cron is locked so nothing should happen
        tracker_id = SettingProperties.get_int('last_tracker_pk', 0)
        self.assertEqual(tracker_id, 0)

        # unlock
        SettingProperties.delete_key('oppia_summary_cron_lock')
        # check unlocked again
        lock = SettingProperties.get_int('oppia_summary_cron_lock', 999)
        self.assertEqual(lock, 999)

    def test_summary_cron_open_cron_locked(self):
        # set locked
        SettingProperties.set_int('oppia_cron_lock', 1)
        lock = SettingProperties.get_int('oppia_cron_lock', 0)
        self.assertEqual(lock, 1)

        lock = SettingProperties.get_int('oppia_summary_cron_lock', 999)
        self.assertEqual(lock, 999)

        call_command('update_summaries', stdout=StringIO())

        # check new details on pks
        # cron is locked so nothing should happen
        tracker_id = SettingProperties.get_int('last_tracker_pk', 0)
        self.assertEqual(tracker_id, 0)

        # unlock
        SettingProperties.delete_key('oppia_cron_lock')
        # check unlocked again
        lock = SettingProperties.get_int('oppia_cron_lock', 999)
        self.assertEqual(lock, 999)

    def test_summary_cron_locked_cron_locked(self):
        # set locked
        SettingProperties.set_int('oppia_cron_lock', 1)
        lock = SettingProperties.get_int('oppia_cron_lock', 0)
        self.assertEqual(lock, 1)

        SettingProperties.set_int('oppia_summary_cron_lock', 1)
        lock = SettingProperties.get_int('oppia_summary_cron_lock', 0)
        self.assertEqual(lock, 1)

        call_command('update_summaries', stdout=StringIO())

        # check new details on pks
        # cron is locked so nothing should happen
        tracker_id = SettingProperties.get_int('last_tracker_pk', 0)
        self.assertEqual(tracker_id, 0)

        # unlock
        SettingProperties.delete_key('oppia_summary_cron_lock')
        SettingProperties.delete_key('oppia_cron_lock')
        # check unlocked again
        lock = SettingProperties.get_int('oppia_summary_cron_lock', 999)
        self.assertEqual(lock, 999)
        lock = SettingProperties.get_int('oppia_cron_lock', 999)
        self.assertEqual(lock, 999)

    def test_summary_from_start(self):
        call_command('update_summaries', '--fromstart', stdout=StringIO())

        # check new details on pks
        tracker_id = SettingProperties.get_int('last_tracker_pk', 0)
        self.assertEqual(tracker_id, 1484221)
        # this id is from the test_tracker data

    def test_summary_invalid_latest_tracker(self):
        SettingProperties.objects.update_or_create(key='last_tracker_pk',
                                                   defaults={"int_value":
                                                             2000000})
        call_command('update_summaries', stdout=StringIO())

        self.assertRaises(Tracker.DoesNotExist)
        # check new details on pks
        tracker_id = SettingProperties.get_int('last_tracker_pk', 0)
        self.assertEqual(tracker_id, 2000000)

    def test_summary_empty_tracker_table(self):
        Tracker.objects.all().delete()
        call_command('update_summaries', stdout=StringIO())

        self.assertRaises(Tracker.DoesNotExist)

    def test_summary_empty_points_table(self):
        Points.objects.all().delete()
        call_command('update_summaries', stdout=StringIO())

        self.assertRaises(Points.DoesNotExist)

    def test_summary_search_tracker(self):
        old_search_count = CourseDailyStats.objects.filter(
            type='search').count()
        call_command('update_summaries', stdout=StringIO())
        new_search_count = CourseDailyStats.objects.filter(
            type='search').count()
        self.assertEqual(old_search_count+1, new_search_count)
