import os

import pytest

from django.urls import reverse
from django.conf import settings
from gamification.models import ActivityGamificationEvent, \
                                CourseGamificationEvent, \
                                MediaGamificationEvent
from oppia.models import Activity, Media
from oppia.test import OppiaTestCase


class GamificationFormsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']
    course_file_path = os.path.join(settings.TEST_RESOURCES, 'ncd1_test_course.zip')
    media_course_file_path = os.path.join(settings.TEST_RESOURCES, 'ref-1.zip')

    B_STR_COURSE_XML = b'Course XML updated'

    def test_gamification_event_form_post_no_change(self):
        data = {
            'events-TOTAL_FORMS': 0,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000
            }
        url = reverse('oppia_gamification_edit_course', args=[1])

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(200, response.status_code)

    def test_gamification_event_form_post_add_course(self):

        # Need to upload the file first to make sure it's properly loaded
        with open(self.course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            self.client.post(reverse('oppia:upload'),
                             {'course_file': course_file})

        data = {
            'events-TOTAL_FORMS': 1,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000,
            'events-__prefix__-level': '',
            'events-__prefix__-event': '',
            'events-__prefix__-points': '',
            'events-__prefix__-reference': '',
            'events-0-level': 'course',
            'events-0-event': 'course_downloaded',
            'events-0-points': 500,
            'events-0-reference': 2,
            'sampleform': ''
            }
        url = reverse('oppia_gamification_edit_course', args=[2])

        course_start_count = CourseGamificationEvent.objects.all().count()

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.B_STR_COURSE_XML in response.content)

        course_end_count = CourseGamificationEvent.objects.all().count()
        # this will be the same since the events are already loaded for the
        # course
        self.assertEqual(course_start_count, course_end_count)

        course_game = CourseGamificationEvent.objects.get(
            course__id=2,
            event='course_downloaded')
        self.assertEqual(500, course_game.points)

    def test_gamification_event_form_post_delete_course(self):

        # Need to upload the file first to make sure it's properly loaded
        with open(self.course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            self.client.post(reverse('oppia:upload'),
                             {'course_file': course_file})

        data = {
            'events-TOTAL_FORMS': 1,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000,
            'events-__prefix__-level': '',
            'events-__prefix__-event': '',
            'events-__prefix__-points': '',
            'events-__prefix__-reference': '',
            'events-0-DELETE': 'on',
            'events-0-level': 'course',
            'events-0-event': 'course_downloaded',
            'events-0-points': 0,
            'events-0-reference': 2,
            'sampleform': ''
            }
        url = reverse('oppia_gamification_edit_course', args=[2])

        course_start_count = CourseGamificationEvent.objects.all().count()

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.B_STR_COURSE_XML in response.content)

        course_end_count = CourseGamificationEvent.objects.all().count()
        # this will be the same since the events are already loaded for the
        # course
        self.assertEqual(course_start_count-1, course_end_count)

        with self.assertRaises(CourseGamificationEvent.DoesNotExist):
            CourseGamificationEvent.objects.get(course__id=2,
                                                event='course_downloaded')

    def test_gamification_event_form_post_add_activity(self):

        # Need to upload the file first to make sure it's properly loaded
        with open(self.course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            self.client.post(reverse('oppia:upload'),
                             {'course_file': course_file})

        # get id for the intro page on first section
        activity = Activity.objects.get(section__order=1,
                                        section__course__id=2,
                                        order=1)

        data = {
            'events-TOTAL_FORMS': 1,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000,
            'events-__prefix__-level': '',
            'events-__prefix__-event': '',
            'events-__prefix__-points': '',
            'events-__prefix__-reference': '',
            'events-0-level': 'activity',
            'events-0-event': 'activity_completed',
            'events-0-points': 100,
            'events-0-reference': activity.id,
            'sampleform': ''
            }
        url = reverse('oppia_gamification_edit_course', args=[2])

        activity_start_count = ActivityGamificationEvent.objects.all().count()

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.B_STR_COURSE_XML in response.content)

        activity_end_count = ActivityGamificationEvent.objects.all().count()
        self.assertEqual(activity_start_count+1, activity_end_count)

    def test_gamification_event_form_post_delete_activity(self):

        # Need to upload the file first to make sure it's properly loaded
        with open(self.course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            self.client.post(reverse('oppia:upload'),
                             {'course_file': course_file})

        # get id for the intro page on first section
        activity = Activity.objects.get(section__order=1,
                                        section__course__id=2,
                                        order=1)

        ActivityGamificationEvent.objects.create(event='activity_completed',
                                                 points=100,
                                                 activity=activity,
                                                 user=self.admin_user)
        data = {
            'events-TOTAL_FORMS': 1,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000,
            'events-__prefix__-level': '',
            'events-__prefix__-event': '',
            'events-__prefix__-points': '',
            'events-__prefix__-reference': '',
            'events-0-DELETE': 'on',
            'events-0-level': 'activity',
            'events-0-event': 'activity_completed',
            'events-0-points': 0,
            'events-0-reference': activity.id,
            'sampleform': ''
            }
        url = reverse('oppia_gamification_edit_course', args=[2])

        activity_start_count = ActivityGamificationEvent.objects.all().count()

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.B_STR_COURSE_XML in response.content)

        activity_end_count = ActivityGamificationEvent.objects.all().count()
        self.assertEqual(activity_start_count-1, activity_end_count)

    def test_gamification_event_form_post_add_media(self):

        # Need to upload the file first to make sure it's properly loaded
        with open(self.media_course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            self.client.post(reverse('oppia:upload'),
                             {'course_file': course_file})

        # get id of media
        media = Media.objects.get(digest='45ad219ead30b9a1818176598f8bbbf9',
                                  course__id=4)

        data = {
            'events-TOTAL_FORMS': 1,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000,
            'events-__prefix__-level': '',
            'events-__prefix__-event': '',
            'events-__prefix__-points': '',
            'events-__prefix__-reference': '',
            'events-0-level': 'media',
            'events-0-event': 'media_started',
            'events-0-points': 100,
            'events-0-reference': media.id,
            'sampleform': ''
            }
        url = reverse('oppia_gamification_edit_course', args=[4])

        media_start_count = MediaGamificationEvent.objects.all().count()

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.B_STR_COURSE_XML in response.content)

        media_end_count = MediaGamificationEvent.objects.all().count()
        self.assertEqual(media_start_count+1, media_end_count)

    def test_gamification_event_form_post_delete_media(self):

        # Need to upload the file first to make sure it's properly loaded
        with open(self.media_course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            self.client.post(reverse('oppia:upload'),
                             {'course_file': course_file})

        # get id of media
        media = Media.objects.get(digest='33f33dc89eac9ba776950ce440bd6269',
                                  course__id=4)

        data = {
            'events-TOTAL_FORMS': 1,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000,
            'events-__prefix__-level': '',
            'events-__prefix__-event': '',
            'events-__prefix__-points': '',
            'events-__prefix__-reference': '',
            'events-0-DELETE': 'on',
            'events-0-level': 'media',
            'events-0-event': 'media_started',
            'events-0-points': 0,
            'events-0-reference': media.id,
            'sampleform': ''
            }
        url = reverse('oppia_gamification_edit_course', args=[4])

        media_start_count = MediaGamificationEvent.objects.all().count()

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.B_STR_COURSE_XML in response.content)

        media_end_count = MediaGamificationEvent.objects.all().count()
        self.assertEqual(media_start_count-1, media_end_count)
