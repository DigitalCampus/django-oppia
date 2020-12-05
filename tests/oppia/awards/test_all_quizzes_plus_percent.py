from django.conf import settings

from oppia.awards import courses_completed
from oppia.models import Award, Tracker

from tests.oppia.awards.award_test_case import AwardsTestCase


class AllQuizzesPlusPercentAwardsTest(AwardsTestCase):

    '''
    BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT
    '''
    # all quizzes no other acts
    def test_all_quizzes_no_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_all_quiz_no_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # some quizzes no other acts
    def test_some_quizzes_no_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_some_quiz_no_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)
        
    # no quizzes no other acts
    def test_no_quizzes_no_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_no_quiz_no_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)

    # all quizzes 50% other acts
    def test_all_quizzes_50pc_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_all_quiz_50pc_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)
        
    # some quizzes 50% other acts
    def test_some_quizzes_50pc_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_some_quiz_50pc_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)
        
    # no quizzes 50% other acts
    def test_no_quizzes_50pc_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_no_quiz_50pc_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)
        
    # all quizzes 80% other acts
    def test_all_quizzes_80pc_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_all_quiz_80pc_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+8, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)
        
    # some quizzes 80% other acts
    def test_some_quizzes_80pc_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_some_quiz_80pc_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+8, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)
        
    # no quizzes 80% other acts
    def test_no_quizzes_80pc_acts(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_no_quiz_80pc_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+8, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start, award_count_end)
        
    # duplicate badges
    def test_all_quizzes_80pc_acts_duplicate_awards(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT

        # Load the test data
        tracker_count_start = self.load_data_helper(
            'all_quizzes_plus_percent/tracker_all_quiz_80pc_acts.json')

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+8, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        courses_completed(24)
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)