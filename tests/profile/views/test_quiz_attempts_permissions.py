from django.urls import reverse
from django.core.exceptions import PermissionDenied
from oppia.test import OppiaTestCase

from tests.defaults import UNAUTHORISED_TEMPLATE


class ProfileQuizAttemptPermissionsViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_quizattempt.json',
                'tests/test_course_permissions.json']

    course_id = 1
    quiz_id = 2
    attempt_id = 140106

    '''
    permissions
     - should be same as the get_user permissions
    '''
    # test profile:user_all_attempts
    def test_profile_user_all_attempts_quiz_admin(self):
        # admin can view all
        self.client.force_login(user=self.admin_user)

        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user,
                     self.normal_user]:
            url = reverse('profile:user_all_attempts', args=[user.id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_profile_user_all_attempts_quiz_staff(self):
        # staff can view all
        self.client.force_login(user=self.staff_user)
        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user,
                     self.normal_user]:
            url = reverse('profile:user_all_attempts', args=[user.id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_profile_user_all_attempts_quiz_teacher(self):
        # teacher can only viewing course activity
        self.client.force_login(user=self.teacher_user)

        # cannot view
        for user in [self.admin_user,
                     self.staff_user]:
            url = reverse('profile:user_all_attempts', args=[user.id])
            response = self.client.get(url)
            self.assertEqual(403, response.status_code)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)

        # can view
        for user in [self.teacher_user,
                     self.normal_user]:
            url = reverse('profile:user_all_attempts', args=[user.id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_profile_user_all_attempts_quiz_user(self):
        # normal user can only view their own
        self.client.force_login(user=self.normal_user)

        # cannot view
        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user]:
            url = reverse('profile:user_all_attempts', args=[user.id])
            response = self.client.get(url)
            self.assertEqual(403, response.status_code)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)

        # can view
        url = reverse('profile:user_all_attempts', args=[self.normal_user.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    # test profile_user_quiz_attempts
    def test_profile_user_quiz_attempts_admin(self):
        # admin can view all
        self.client.force_login(user=self.admin_user)

        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user,
                     self.normal_user]:

            url = reverse('profile:user_quiz_attempts', args=[user.id,
                                                              self.course_id,
                                                              self.quiz_id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_profile_user_quiz_attempts_staff(self):
        # staff can view all
        self.client.force_login(user=self.staff_user)
        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user,
                     self.normal_user]:
            url = reverse('profile:user_quiz_attempts', args=[user.id,
                                                              self.course_id,
                                                              self.quiz_id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_profile_user_quiz_attempts_teacher(self):
        # teacher can only viewing course activity
        self.client.force_login(user=self.teacher_user)

        # cannot view
        for user in [self.admin_user,
                     self.staff_user]:
            url = reverse('profile:user_quiz_attempts', args=[user.id,
                                                              self.course_id,
                                                              self.quiz_id])
            response = self.client.get(url)
            self.assertRaises(PermissionDenied)
            self.assertEqual(403, response.status_code)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)

        # can view
        for user in [self.teacher_user,
                     self.normal_user]:
            url = reverse('profile:user_quiz_attempts', args=[user.id,
                                                              self.course_id,
                                                              self.quiz_id])
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_profile_user_quiz_attempts_user(self):
        # normal user can only view their own
        self.client.force_login(user=self.normal_user)

        # cannot view
        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user]:
            url = reverse('profile:user_quiz_attempts', args=[user.id,
                                                              self.course_id,
                                                              self.quiz_id])
            response = self.client.get(url)
            self.assertRaises(PermissionDenied)
            self.assertEqual(403, response.status_code)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)

        # can view
        url = reverse('profile:user_quiz_attempts', args=[self.normal_user.id,
                                                          self.course_id,
                                                          self.quiz_id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    '''
    test profile_user_quiz_attempt_detail
    '''
    def test_profile_user_quiz_attempt_detail_admin(self):
        # admin can view all
        self.client.force_login(user=self.admin_user)

        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user]:

            url = reverse('profile:quiz_attempt_detail',
                          args=[user.id,
                                self.course_id,
                                self.quiz_id,
                                self.attempt_id])
            response = self.client.get(url)
            self.assertEqual(404, response.status_code)

        # user - found
        url = reverse('profile:quiz_attempt_detail',
                      args=[self.normal_user.id,
                            self.course_id,
                            self.quiz_id,
                            self.attempt_id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_profile_user_quiz_attempt_detail_staff(self):
        # staff can view all
        self.client.force_login(user=self.staff_user)
        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user]:
            url = reverse('profile:quiz_attempt_detail',
                          args=[user.id,
                                self.course_id,
                                self.quiz_id,
                                self.attempt_id])
            response = self.client.get(url)
            self.assertEqual(404, response.status_code)

        # user - found
        url = reverse('profile:quiz_attempt_detail',
                      args=[self.normal_user.id,
                            self.course_id,
                            self.quiz_id,
                            self.attempt_id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_profile_user_quiz_attempt_detail_teacher(self):
        # teacher can only viewing course activity
        self.client.force_login(user=self.teacher_user)

        # not found for user
        for user in [self.admin_user,
                     self.staff_user]:
            url = reverse('profile:quiz_attempt_detail',
                          args=[user.id,
                                self.course_id,
                                self.quiz_id,
                                self.attempt_id])
            response = self.client.get(url)
            self.assertEqual(403, response.status_code)

        # teacher - not found
        url = reverse('profile:quiz_attempt_detail',
                      args=[self.teacher_user.id,
                            self.course_id,
                            self.quiz_id,
                            self.attempt_id])
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

        # user - found
        url = reverse('profile:quiz_attempt_detail',
                      args=[self.normal_user.id,
                            self.course_id,
                            self.quiz_id,
                            self.attempt_id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_profile_user_quiz_attempt_detail_user(self):
        # normal user can only view their own
        self.client.force_login(user=self.normal_user)

        # cannot view
        for user in [self.admin_user,
                     self.staff_user,
                     self.teacher_user]:
            url = reverse('profile:quiz_attempt_detail',
                          args=[user.id,
                                self.course_id,
                                self.quiz_id,
                                self.attempt_id])
            response = self.client.get(url)
            self.assertRaises(PermissionDenied)
            self.assertEqual(403, response.status_code)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)

        # can view
        url = reverse('profile:quiz_attempt_detail',
                      args=[self.normal_user.id,
                            self.course_id,
                            self.quiz_id,
                            self.attempt_id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
