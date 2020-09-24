import pytest

from django.urls import reverse
from gamification.models import CourseGamificationEvent, \
                                MediaGamificationEvent, \
                                ActivityGamificationEvent
from oppia.test import OppiaTestCase
from oppia.models import Course, CoursePublishingLog
from zipfile import BadZipfile


class CourseUploadTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']
    file_root = './oppia/fixtures/reference_files/'
    course_file_path = file_root + 'ncd1_test_course.zip'
    media_file_path = file_root + 'sample_video.m4v'
    empty_section_course = file_root + 'test_course_empty_section.zip'
    no_module_xml = file_root + 'test_course_no_module_xml.zip'
    corrupt_course_zip = file_root + 'corrupt_course.zip'
    course_no_sub_dir = file_root + 'test_course_no_sub_dir.zip'
    course_old_version = file_root + 'ncd1_old_course.zip'
    course_no_activities = file_root + 'test_course_no_activities.zip'
    course_with_custom_points = file_root + 'ref-1.zip'
    course_with_custom_points_updated = file_root + 'ref-1-updated.zip'

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_upload_template(self):

        with open(self.course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})
            # should be redirected to the update step 2 form
            self.assertRedirects(response,
                                 reverse('oppia:upload_step2', args=[2]),
                                 302,
                                 200)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_upload_with_empty_sections(self):

        with open(self.empty_section_course, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})

            course = Course.objects.latest('created_date')
            # should be redirected to the update step 2 form
            self.assertRedirects(response,
                                 reverse('oppia:upload_step2',
                                         args=[course.id]),
                                 302,
                                 200)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_upload_no_module_xml(self):

        with open(self.no_module_xml, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("no_module_xml", course_log.action)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_corrupt_course(self):

        with open(self.corrupt_course_zip, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            self.assertRaises(BadZipfile)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("invalid_zip", course_log.action)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_no_sub_dir(self):

        with open(self.course_no_sub_dir, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("invalid_zip", course_log.action)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_newer_version_exists(self):

        with open(self.course_old_version, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("newer_version_exists", course_log.action)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_course_no_activities(self):

        with open(self.course_no_activities, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("no_activities", course_log.action)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_course_with_custom_points(self):

        course_game_events_start = CourseGamificationEvent. \
            objects.all().count()
        media_game_events_start = MediaGamificationEvent. \
            objects.all().count()
        activity_game_events_start = ActivityGamificationEvent. \
            objects.all().count()

        with open(self.course_with_custom_points, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse('oppia:upload_step2',
                                         args=[course.id]),
                                 302,
                                 200)

        course_game_events_end = CourseGamificationEvent.objects.all().count()
        self.assertEqual(course_game_events_start+10, course_game_events_end)

        media_game_events_end = MediaGamificationEvent.objects.all().count()
        self.assertEqual(media_game_events_start+4, media_game_events_end)

        activity_game_events_end = ActivityGamificationEvent. \
            objects.all().count()
        self.assertEqual(activity_game_events_start+1,
                         activity_game_events_end)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_course_with_custom_points_updated(self):

        with open(self.course_with_custom_points, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse('oppia:upload_step2',
                                         args=[course.id]),
                                 302,
                                 200)

        course_game_events_start = CourseGamificationEvent. \
            objects.all().count()
        media_game_events_start = MediaGamificationEvent. \
            objects.all().count()
        activity_game_events_start = ActivityGamificationEvent. \
            objects.all().count()

        # reset course version no to avoid issue with newer version being
        # reported in the test
        update_course = Course.objects.get(shortname='ref-1')
        update_course.version = 0
        update_course.save()

        with open(self.course_with_custom_points_updated, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia:upload'),
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse('oppia:upload_step2',
                                         args=[course.id]),
                                 302,
                                 200)
        course_game_events_end = CourseGamificationEvent.objects.all().count()
        self.assertEqual(course_game_events_start, course_game_events_end)

        media_game_events_end = MediaGamificationEvent.objects.all().count()
        self.assertEqual(media_game_events_start, media_game_events_end)

        activity_game_events_end = ActivityGamificationEvent. \
            objects.all().count()
        self.assertEqual(activity_game_events_start, activity_game_events_end)
