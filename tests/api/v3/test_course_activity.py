import os
import shutil
import unittest
import pytest

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from rest_framework.test import APITestCase

from oppia.models import Tracker, Course, CourseStatus
from tests.utils import update_course_status, update_course_owner
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

    url = '/api/v3/course/'

    STR_ACTIVITY = 'activity/'
    TEST_COURSES = ['anc_test_course.zip']

    def setUp(self):
        super(CourseActivityAPITests, self).setUp()
        self.copy_test_courses()
        self.teacher = User.objects.get(username="teacher")

    def perform_download_request(self, course_id, headers):
        resource_url = self.download_url + str(course_id) + "/"
        response = self.client.get(resource_url, headers=headers)
        return response

    def test_course_get_activity(self):
        resp = self.perform_request(1, self.user_auth, self.STR_ACTIVITY)
        self.assertHttpOK(resp)
        xml_doc = ET.fromstring(resp.content)
        trackers = xml_doc.findall("tracker")
        self.assertEqual(276, len(trackers))
        first_tracker = trackers[0]
        self.assertEqual('cd646d1148da0f45cd4f097c6761186b17687', first_tracker.get('digest'))
        self.assertEqual('2015-04-16 13:01:59', first_tracker.get('submitteddate'))
        self.assertTrue(first_tracker.get('completed'))
        self.assertEqual('page', first_tracker.get('type'))
        self.assertEqual('', first_tracker.get('event'))
        self.assertEqual('None', first_tracker.get('points'))

    def test_course_get_activity_notfound(self):
        resp = self.perform_request(999, self.user_auth, self.STR_ACTIVITY)
        self.assertHttpNotFound(resp)

    def test_course_get_activity_draft_nonvisible(self):
        resp = self.perform_request(3, self.user_auth, self.STR_ACTIVITY)
        self.assertHttpNotFound(resp)

    def test_course_get_activity_draft_admin_visible(self):
        resp = self.perform_request(3, self.admin_auth, self.STR_ACTIVITY)
        self.assertHttpOK(resp)
