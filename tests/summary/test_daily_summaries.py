from django.core.management import call_command

from io import StringIO

from django.contrib.auth.models import User
from django.db.models import Sum

from oppia.test import OppiaTestCase
from oppia.models import Course
from summary.models import UserCourseDailySummary

# View test_usercoursesummary for course trackers description

COURSE_SHORTNAME = "oppia800course"

JSON_GAMIFICATION = 'default_gamification_events.json'
JSON_BADGES = 'default_badges.json'
JSON_USERS = 'tests/usercoursesummary/user.json'


class UserCourseSummaryTestCourseV1(OppiaTestCase):

    fixtures = [JSON_GAMIFICATION, JSON_BADGES, JSON_USERS,
                'tests/usercoursesummary/course_tracker_v1.json']

    def setUp(self):
        self.course = Course.objects.get(shortname=COURSE_SHORTNAME)
        self.user_a = User.objects.get(username="user_a")
        self.user_b = User.objects.get(username="user_b")
        self.user_c = User.objects.get(username="user_c")

    def test_incremental(self):
        call_command('update_summaries', stdout=StringIO())

        stats = UserCourseDailySummary.objects.filter(course__shortname=COURSE_SHORTNAME)
        self.assertEqual(stats.count(), 4)

        totals = stats.aggregate(submitted=Sum('total_submitted'), tracked=Sum('total_tracked'))
        # After the process, the number of submitted and tracked stats should be the same
        self.assertEqual(totals['submitted'], totals['tracked'])
