# coding: utf-8

from django.urls import reverse

from oppia.test import OppiaTestCase


class QuizDownloadTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_quizattempt.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']
    STR_EXPECTED_CONTENT_TYPE = 'application/vnd.ms-excel;charset=utf-8'
    STR_URL_TEMPLATE = 'quiz:quiz_results_download'
    STR_URL_OLD_QUIZ_TEMPLATE = 'quiz:old_quiz_results_download'

    valid_course_valid_quiz_url = reverse(STR_URL_TEMPLATE,
                                          args=[1, 18])
    invalid_course_valid_quiz_url = reverse(STR_URL_TEMPLATE,
                                            args=[0, 18])
    valid_course_invalid_quiz_url = reverse(STR_URL_TEMPLATE,
                                            args=[1, 0])
    invalid_course_invalid_quiz_url = reverse(STR_URL_TEMPLATE,
                                              args=[0, 0])
    course_quiz_mismatch_url = reverse(STR_URL_TEMPLATE,
                                       args=[1, 224])

    def test_admin_download(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_valid_quiz_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE,
                         response['content-type'])

    def test_staff_download(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_valid_quiz_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE,
                         response['content-type'])

    def test_teacher_download(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_valid_quiz_url)
        self.assertTemplateUsed(response, self.unauthorized_template)
        self.assertEqual(403, response.status_code)

    def test_user_download(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_valid_quiz_url)
        self.assertTemplateUsed(response, self.unauthorized_template)
        self.assertEqual(403, response.status_code)

    def test_invalid_course_valid_quiz(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            self.client.force_login(user)
            response = self.client.get(self.invalid_course_valid_quiz_url)
            self.assertEqual(404, response.status_code)

    def test_valid_course_invalid_quiz(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            self.client.force_login(user)
            response = self.client.get(self.valid_course_invalid_quiz_url)
            self.assertEqual(404, response.status_code)

    def test_invalid_course_invalid_quiz(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            self.client.force_login(user)
            response = self.client.get(self.invalid_course_invalid_quiz_url)
            self.assertEqual(404, response.status_code)

    def test_course_quiz_mismatch(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            self.client.force_login(user)
            response = self.client.get(self.course_quiz_mismatch_url)
            self.assertEqual(404, response.status_code)
    
    def test_old_quiz_download(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse(self.STR_URL_OLD_QUIZ_TEMPLATE,
                                           args=[1, 18]))
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE,
                         response['content-type'])
