from django.conf import settings
from django.urls import reverse

from oppia.awards import courses_completed
from oppia.models import Award, Tracker
from oppia.test import OppiaTestCase


'''
badge not loaded
'''


class AwardsNoBadgesTest(OppiaTestCase):

    def setUp(self):
        super(AwardsNoBadgesTest, self).setUp()

    def test_badges_not_loaded(self):
        result = courses_completed(0)
        self.assertFalse(result)


class AwardsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json']
    file_root = './oppia/fixtures/tests/awards/'
    url = reverse('activitylog:upload')

    '''
    BADGE_AWARD_METHOD_ALL_ACTIVITIES
    '''
    # all activities completed and passed
    def test_all_acts_all_complete(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES

        # Load the test data
        tracker_file = self.file_root + 'tracker_all_acts_all_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)

    # all activities attempted, but not all complete
    def test_all_acts_some_complete(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES

        # Load the test data
        tracker_file = self.file_root + 'tracker_all_acts_some_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + 'tracker_all_acts_some_attempted.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_all_attempted_none_completed.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + 'tracker_all_acts_all_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+7, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        # the the script again
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)

    '''
    BADGE_AWARD_METHOD_FINAL_QUIZ
    '''
    # final quiz attempted and passed
    def test_final_quiz_passed(self):
        settings.BADGE_AWARDING_METHOD = settings.BADGE_AWARD_METHOD_FINAL_QUIZ

        # Load the test data
        tracker_file = self.file_root + 'tracker_final_quiz_passed.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_all_attempted_none_completed.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_final_quiz_some_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_final_quiz_attempted.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + 'tracker_final_quiz_passed.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        courses_completed(24)
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)

    '''
    BADGE_AWARD_METHOD_ALL_QUIZZES
    '''
    # both quizzes passed
    def test_all_quiz_passed(self):
        settings.BADGE_AWARDING_METHOD = \
            settings.BADGE_AWARD_METHOD_ALL_QUIZZES

        # Load the test data
        tracker_file = self.file_root + 'tracker_all_quizzes_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_all_quizzes_none_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_all_quizzes_some_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_all_quizzes_one_passed.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + \
            'tracker_all_quizzes_attempted_only.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

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
        tracker_file = self.file_root + 'tracker_all_quizzes_complete.json'
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+2, tracker_count_end)

        award_count_start = Award.objects.all().count()
        courses_completed(0)
        courses_completed(24)
        courses_completed(0)
        award_count_end = Award.objects.all().count()
        self.assertEqual(award_count_start+1, award_count_end)
