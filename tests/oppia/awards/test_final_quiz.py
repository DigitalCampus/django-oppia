from django.conf import settings

from oppia.awards import courses_completed
from oppia.models import Award, Tracker

from tests.oppia.awards.award_test_case import AwardsTestCase


class FinalQuizAwardsTest(AwardsTestCase):

    '''
    BADGE_AWARD_METHOD_FINAL_QUIZ
    '''
    # final quiz attempted and passed
    def test_final_quiz_passed(self):
        settings.BADGE_AWARDING_METHOD = settings.BADGE_AWARD_METHOD_FINAL_QUIZ

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'final_quiz/tracker_final_quiz_passed.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)

    # no activities completed
    def test_final_quiz_none_completed(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_FINAL_QUIZ

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'final_quiz/tracker_all_attempted_none_completed.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+6, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # some other activities completed but not final quiz
    def test_final_quiz_some_completed(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_FINAL_QUIZ

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'final_quiz/tracker_final_quiz_some_complete.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+5, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # final quiz attempted but not passed
    def test_final_quiz_attempted(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_FINAL_QUIZ

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'final_quiz/tracker_final_quiz_attempted.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+6, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # check badge cannot be awarded twice
    def test_final_quiz_duplicate_awards(self):
        settings.BADGE_AWARDING_METHOD = settings.BADGE_AWARD_METHOD_FINAL_QUIZ

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'final_quiz/tracker_final_quiz_passed.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        courses_completed(24)
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)