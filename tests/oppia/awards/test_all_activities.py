from django.conf import settings

from oppia.awards import courses_completed
from oppia.models import Award, Tracker

from tests.oppia.awards.award_test_case import AwardsTestCase


class AllActivitiesAwardsTest(AwardsTestCase):

    '''
    BADGE_AWARD_METHOD_ALL_ACTIVITIES
    '''
    # all activities completed and passed
    def test_all_acts_all_complete(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_activities/tracker_all_acts_all_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+8, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)

    # all activities attempted, but not all complete
    def test_all_acts_some_complete(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_activities/tracker_all_acts_some_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # not all activities attempted
    def test_all_acts_some_attempted(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_activities/tracker_all_acts_some_attempted.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+5, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # no activities completed
    def test_all_acts_none_completed(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_activities/tracker_all_attempted_none_completed.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+6, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # check badge cannot be awarded twice
    def test_all_acts_duplicate_awards(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_activities/tracker_all_acts_all_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+8, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        courses_completed(24)
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)