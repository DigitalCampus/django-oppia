import datetime

from oppia.test import OppiaTestCase
from django.urls import reverse
from django.utils import timezone

from viz.views import summary_get_registrations, \
                      summary_get_countries, \
                      summary_get_languages, \
                      summary_get_downloads, \
                      summary_get_course_activity, \
                      summary_get_searches


class VisualisationsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_viz.json',
                'default_gamification_events.json',
                'tests/test_tracker.json']

    # summary
    # only staff/admins can view
    def test_view_summary(self):
        allowed_users = [self.admin_user, self.staff_user]
        disallowed_users = [self.teacher_user, self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(reverse('oppia_viz_summary'))

            self.assertTemplateUsed(response, 'viz/summary.html')
            self.assertEqual(response.status_code, 200)

        for disallowed_user in disallowed_users:
            self.client.force_login(disallowed_user)
            response = self.client.get(reverse('oppia_viz_summary'))
            self.assertEqual(response.status_code, 302)

    # test posting dates (
    def test_view_summary_previous_date(self):
        self.client.force_login(self.admin_user)
        start_date = timezone.now() - datetime.timedelta(days=31)
        response = self.client.post(reverse('oppia_viz_summary'),
                                    data={'start_date': start_date})
        self.assertTemplateUsed(response, 'viz/summary.html')
        self.assertEqual(response.status_code, 200)

    def test_view_summary_future_date(self):
        self.client.force_login(self.admin_user)
        start_date = timezone.now() + datetime.timedelta(days=31)
        response = self.client.post(reverse('oppia_viz_summary'),
                                    data={'start_date': start_date})
        self.assertTemplateUsed(response, 'viz/summary.html')
        self.assertEqual(response.status_code, 200)

    def test_view_summary_invalid_date(self):
        self.client.force_login(self.admin_user)
        start_date = "not a valid date"
        response = self.client.post(reverse('oppia_viz_summary'),
                                    data={'start_date': start_date})
        self.assertTemplateUsed(response, 'viz/summary.html')
        self.assertEqual(response.status_code, 200)

    # map
    def test_view_map(self):

        allowed_users = [self.admin_user,
                         self.teacher_user,
                         self.staff_user,
                         self.normal_user,]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(reverse('oppia_viz_map'))
            self.assertTemplateUsed(response, 'viz/map.html')
            self.assertEqual(response.status_code, 200)

    # test summary helper methods
    def test_summary_helper_reg(self):
        start_date = timezone.now() - datetime.timedelta(days=365)

        user_registrations, previous_user_registrations = \
            summary_get_registrations(start_date)
        self.assertEqual(user_registrations.count(), 0)
        self.assertEqual(previous_user_registrations, 4)

    def test_summary_helper_countries(self):
        start_date = timezone.now() - datetime.timedelta(days=365)
        # Countries
        total_countries, country_activity = summary_get_countries(start_date)
        self.assertEqual(len(country_activity), 21)
        self.assertEqual(total_countries, 51)

    def test_summary_helper_langs(self):
        start_date = timezone.now() - datetime.timedelta(days=365)
        # Language
        languages = summary_get_languages(start_date)
        self.assertEqual(len(languages), 3)

    def test_summary_helper_downloads(self):
        start_date = timezone.now() - datetime.timedelta(days=365)
        # Course Downloads
        course_downloads, previous_course_downloads = \
            summary_get_downloads(start_date)
        self.assertEqual(course_downloads.count(), 0)
        self.assertEqual(previous_course_downloads, 0)

    def test_summary_helper_activity(self):
        start_date = timezone.now() - datetime.timedelta(days=365)
        # Course Activity
        course_activity, previous_course_activity, hot_courses = \
            summary_get_course_activity(start_date)
        self.assertEqual(course_activity.count(), 0)
        self.assertEqual(previous_course_activity, 0)
        self.assertEqual(len(hot_courses), 0)

    def test_summary_helper_search(self):
        start_date = timezone.now() - datetime.timedelta(days=365)
        # Searches
        searches, previous_searches = summary_get_searches(start_date)
        self.assertEqual(searches.count(), 0)
        self.assertEqual(previous_searches, 0)
