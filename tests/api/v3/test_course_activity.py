
import unittest
import pytest


from rest_framework.test import APITestCase

from tests.api.v3 import utils


class CourseActivityAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json',
                'tests/test_cohort.json',
                'tests/test_progress_summary.json',
                'tests/test_tracker.json']

    # @TODO confirm final endpoint for getting course activity
    activity_url = '/api/v3/course/activity/'

    def perform_activity_request(self, course_ref, headers):
        resource_url = self.activity_url + str(course_ref) + "/"
        response = self.client.get(resource_url, headers=headers)
        return response

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_activity(self):
        response = self.perform_activity_request(1, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        trackers = response.json()
        self.assertEqual(276, len(trackers))
        first_tracker = trackers[0]
        self.assertEqual('cd646d1148da0f45cd4f097c6761186b17687', first_tracker.get('digest'))
        self.assertEqual('2015-04-16 13:01:59', first_tracker.get('submitteddate'))
        self.assertTrue(first_tracker.get('completed'))
        self.assertEqual('page', first_tracker.get('type'))
        self.assertEqual('', first_tracker.get('event'))
        self.assertEqual('None', first_tracker.get('points'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_activity_notfound(self):
        response = self.perform_activity_request(999, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_activity_draft_nonvisible(self):
        response = self.perform_activity_request(3, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_get_activity_draft_admin_visible(self):
        response = self.perform_activity_request(3, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
