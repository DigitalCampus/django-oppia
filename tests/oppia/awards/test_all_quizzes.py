from django.conf import settings

from oppia.awards import courses_completed
from oppia.models import Award, Tracker

from tests.oppia.awards.award_test_case import AwardsTestCase


class AllQuizzesAwardsTest(AwardsTestCase):


    '''
    BADGE_AWARD_METHOD_ALL_QUIZZES
    '''
    # both quizzes passed
    def test_all_quiz_passed(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_QUIZZES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes/tracker_all_quizzes_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+2, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)

    # no activities completed
    def test_all_quiz_none_complete(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_QUIZZES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes/tracker_all_quizzes_none_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+6, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # some other activities completed but not quizzes
    def test_all_quiz_some_activities_complete(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_QUIZZES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes/tracker_all_quizzes_some_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+6, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # one quiz passed and the other not attempted
    def test_all_quiz_some_complete(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_QUIZZES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes/tracker_all_quizzes_one_passed.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+5, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # both quizzes attempted but not passed
    def test_all_quiz_attempted_only(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_QUIZZES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes/tracker_all_quizzes_attempted_only.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+6, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # check badge cannot be awarded twice
    def test_all_quiz_duplicate_awards(self):

        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_QUIZZES

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes/tracker_all_quizzes_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+2, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        courses_completed(24)
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)
        