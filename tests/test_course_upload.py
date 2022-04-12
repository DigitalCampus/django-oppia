import os

import pytest

from django.urls import reverse
from django.conf import settings
from gamification.models import CourseGamificationEvent, \
                                MediaGamificationEvent, \
                                ActivityGamificationEvent
from oppia.test import OppiaTestCase
from oppia.models import Course, CoursePublishingLog, Quiz, Activity, Question
from zipfile import BadZipfile

from quiz.models import QuizProps, QuestionProps


class CourseUploadTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    course_file_path = os.path.join(settings.TEST_RESOURCES, 'ncd1_test_course.zip')
    media_file_path = os.path.join(settings.TEST_RESOURCES, 'sample_video.m4v')
    empty_section_course = os.path.join(settings.TEST_RESOURCES, 'test_course_empty_section.zip')
    no_module_xml = os.path.join(settings.TEST_RESOURCES, 'test_course_no_module_xml.zip')
    corrupt_course_zip = os.path.join(settings.TEST_RESOURCES, 'corrupt_course.zip')
    course_no_sub_dir = os.path.join(settings.TEST_RESOURCES, 'test_course_no_sub_dir.zip')
    course_old_version = os.path.join(settings.TEST_RESOURCES, 'ncd1_old_course.zip')
    course_no_activities = os.path.join(settings.TEST_RESOURCES, 'test_course_no_activities.zip')
    course_with_custom_points = os.path.join(settings.TEST_RESOURCES, 'ref-1.zip')
    course_with_copied_activities = os.path.join(settings.TEST_RESOURCES, 'ref-1-copy.zip')
    course_with_custom_points_updated = os.path.join(settings.TEST_RESOURCES, 'ref-1-updated.zip')
    course_with_quizprops = os.path.join(settings.TEST_RESOURCES, 'quizprops_course.zip')
    course_with_updated_quizprops = os.path.join(settings.TEST_RESOURCES, 'quizprops_course_updated.zip')

    URL_UPLOAD = reverse('oppia:upload')
    STR_UPLOAD_STEP2 = 'oppia:upload_step2'

    def test_upload_template(self):

        with open(self.course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})
            # should be redirected to the update step 2 form
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2, args=[2]),
                                 302,
                                 200)

    def test_upload_with_empty_sections(self):

        with open(self.empty_section_course, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})

            course = Course.objects.latest('created_date')
            # should be redirected to the update step 2 form
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2,
                                         args=[course.id]),
                                 302,
                                 200)

    def test_upload_no_module_xml(self):

        with open(self.no_module_xml, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("no_module_xml", course_log.action)

    def test_corrupt_course(self):

        with open(self.corrupt_course_zip, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            self.assertRaises(BadZipfile)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("invalid_zip", course_log.action)

    def test_no_sub_dir(self):

        with open(self.course_no_sub_dir, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("invalid_zip", course_log.action)

    def test_newer_version_exists(self):

        with open(self.course_old_version, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("newer_version_exists", course_log.action)

    def test_course_no_activities(self):

        with open(self.course_no_activities, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("no_activities", course_log.action)

    def test_course_with_custom_points(self):

        course_game_events_start = CourseGamificationEvent. \
            objects.all().count()
        media_game_events_start = MediaGamificationEvent. \
            objects.all().count()
        activity_game_events_start = ActivityGamificationEvent. \
            objects.all().count()

        with open(self.course_with_custom_points, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2,
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

    def test_course_with_custom_points_updated(self):

        with open(self.course_with_custom_points, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2,
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
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2,
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

    def test_update_quizprops(self):
        self.client.force_login(self.admin_user)

        with open(self.course_with_quizprops, 'rb') as course_file:

            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})

            course = Course.objects.get(shortname='quizprops_course')
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2,
                                         args=[course.id]),
                                 302,
                                 200)

            current_quizzes = Activity.objects.filter(
                section__course=course,
                type=Activity.QUIZ).values_list('digest', flat=True)
            quizzes = Quiz.objects.filter(
                quizprops__name='digest',
                quizprops__value__in=current_quizzes)
            quiz_questions = Question.objects.filter(
                quizquestion__quiz__in=quizzes)
            quiz_props = QuizProps.objects.filter(quiz__in=quizzes)
            question_props = QuestionProps.objects.filter(
                question__in=quiz_questions)

            self.assertEqual(1, quizzes.count())
            self.assertEqual(2, quiz_questions.count())
            self.assertEqual(8, quiz_props.count())
            self.assertEqual(4, question_props.count())
            self.assertEqual(QuizProps.objects.filter(
                name='moodle_quiz_id',
                quiz=quizzes.first()).first().value, '43504')

            # Lower the version so that we can upload a new one regardless of
            # the current date
            course.version = 100
            course.save()

        with open(self.course_with_updated_quizprops, 'rb') as course_file:
            course = Course.objects.get(shortname='quizprops_course')

            self.client.post(reverse('oppia:upload'),
                             {'course_file': course_file})
            current_quizzes = Activity.objects.filter(
                section__course=course,
                type=Activity.QUIZ).values_list('digest', flat=True)
            quizzes = Quiz.objects.filter(quizprops__name='digest',
                                          quizprops__value__in=current_quizzes)
            quiz_questions = Question.objects.filter(
                quizquestion__quiz__in=quizzes)
            quiz_props = QuizProps.objects.filter(quiz__in=quizzes)
            question_props = QuestionProps.objects.filter(
                question__in=quiz_questions)

            # Assert that no new quizzes or props were created, only updated
            self.assertEqual(1, quizzes.count())
            self.assertEqual(2, quiz_questions.count())
            self.assertEqual(8, quiz_props.count())

            # Additional question prop added
            self.assertEqual(5, question_props.count())
            self.assertEqual(QuizProps.objects.filter(
                name='moodle_quiz_id',
                quiz=quizzes.first()).first().value,
                '43505')  # property updated

    def test_course_with_repeated_activities(self):
        with open(self.course_with_custom_points, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2,
                                         args=[course.id]), 302, 200)

        course_activities = Activity.objects.filter(
            section__course__shortname='ref-1').count()
        self.assertEqual(course_activities, 5)

        with open(self.course_with_copied_activities, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(self.URL_UPLOAD,
                                        {'course_file': course_file})
            course = Course.objects.latest('created_date')
            self.assertRedirects(response,
                                 reverse(self.STR_UPLOAD_STEP2,
                                         args=[course.id]), 302, 200)

        course_activities = Activity.objects.filter(
            section__course__shortname='ref-1').count()
        new_course_activities = Activity.objects.filter(
            section__course__shortname='ref-1-copy').count()

        self.assertEqual(new_course_activities, 5)
        self.assertEqual(course_activities, 5)
