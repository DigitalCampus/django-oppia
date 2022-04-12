import os

from django.conf import settings
from django.urls import reverse

from oppia.awards import courses_completed
from oppia.test import OppiaTestCase
from oppia.models import Tracker, Award, Points, BadgeMethod, Badge


class AwardsTestCase(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json',
                'tests/test_settings.json']
    file_root = os.path.join(settings.FIXTURES_PATH, 'tests', 'awards')
    url = reverse('activitylog:upload')

    def set_badge_method(self, method, course=None):
        badge_method = BadgeMethod.objects.get(key=method)
        badge = Badge.objects.get(ref='coursecompleted')
        badge.default_method = badge_method
        badge.save()

    def load_trackers(self, file, plus_trackers=0):
        tracker_file = os.path.join(self.file_root, file)
        self.client.force_login(self.admin_user)

        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+plus_trackers, tracker_count_end)
        return tracker_count_start

    def assert_points_and_awards(self, plus_awards=0, plus_points=0, hours=0):

        points_count_start = Points.objects.all().count()
        award_count_start = Award.objects.all().count()
        courses_completed(hours)
        award_count_end = Award.objects.all().count()
        points_count_end = Points.objects.all().count()
        self.assertEqual(award_count_start+plus_awards, award_count_end)
        self.assertEqual(points_count_start+plus_points, points_count_end)
