from oppia.test import OppiaTestCase
from settings.models import SettingProperties
from summary.cron import update_summaries


class SummaryCronTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'default_badges.json']

    def test_summary_cron_open_cron_open(self):
        # check lock not set
        lock = SettingProperties.get_int('oppia_summary_cron_lock', 999)
        self.assertEqual(lock, 999)
        lock = SettingProperties.get_int('oppia_cron_lock', 999)
        self.assertEqual(lock, 999)

        update_summaries()

        # check new details on pks
        tracker_id = SettingProperties.get_int('last_tracker_pk', 0)
        self.assertEqual(tracker_id, 1472216)
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

        update_summaries()

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

        update_summaries()

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

        update_summaries()

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
