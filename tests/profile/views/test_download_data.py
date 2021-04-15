from django.urls import reverse
from oppia.test import OppiaTestCase


class DownloadDataViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_cohort.json',
                'tests/test_customfields.json',
                'tests/test_quiz.json',
                'tests/test_quizattempt.json']
    
    STR_EXPECTED_CONTENT_TYPE = 'text/html; charset=utf-8'
    STR_URL = 'profile:export_mydata'
    
    def test_invalid_download(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse(self.STR_URL,
                                           args=['invalid']))
        self.assertEqual(404, response.status_code)
            
    def test_profile(self):
        for user in [self.normal_user,
                     self.admin_user,
                     self.teacher_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL,
                                               args=['profile']))
            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed('profile/export/profile.html')
            self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    def test_points(self):
        for user in [self.normal_user,
                     self.admin_user,
                     self.teacher_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL,
                                               args=['points']))
            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed('profile/export/points.html')
            self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
    
    def test_badges(self):
        for user in [self.normal_user,
                     self.admin_user,
                     self.teacher_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL,
                                               args=['badges']))
            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed('profile/export/badges.html')
            self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    def test_quiz(self):
        for user in [self.normal_user,
                     self.admin_user,
                     self.teacher_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL,
                                               args=['quiz']))
            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed('profile/export/quiz.html')
            self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    def test_activity(self):
        for user in [self.normal_user,
                     self.admin_user,
                     self.teacher_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL,
                                               args=['activity']))
            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed('profile/export/activity.html')
            self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)