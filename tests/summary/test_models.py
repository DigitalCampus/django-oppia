
from oppia.test import OppiaTestCase
from summary.models import DailyActiveUsers


class SummaryModelTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'default_badges.json',
                'tests/test_search_tracker.json',
                'tests/test_course_permissions.json',
                'tests/test_daus.json']

    def test_total_time(self):
        dau = DailyActiveUsers.objects.get(day__day=27,
                                           day__month=2,
                                           day__year=2015)
        total_time = dau.get_total_time_spent()
        self.assertEqual(381, total_time)

    def test_avg_time(self):
        dau = DailyActiveUsers.objects.get(day__day=27,
                                           day__month=2,
                                           day__year=2015)
        avg_time = dau.get_avg_time_spent()
        self.assertEqual(190.5, avg_time)
