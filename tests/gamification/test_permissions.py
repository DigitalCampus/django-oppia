
from django.urls import reverse

from oppia.models import CourseStatus
from oppia.test import OppiaTestCase
from tests.utils import update_course_status


class GamificationPermissionsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_course_permissions.json']
    valid_course_url = reverse('oppia_gamification_edit_course', args=[1])
    invalid_course_url = reverse('oppia_gamification_edit_course', args=[55])

    def testCoursePointsEdit(self):
        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

    def testUnknownCoursePointsEdit(self):

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 403)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 403)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 403)

    def test_can_edit_gamification_live_course(self):
        update_course_status(1, CourseStatus.LIVE)

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

    def test_can_edit_gamification_draft_course(self):
        update_course_status(1, CourseStatus.DRAFT)

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

    def test_can_edit_gamification_archived_course(self):
        update_course_status(1, CourseStatus.ARCHIVED)

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

    def test_can_edit_gamification_new_downloads_disabled_course(self):
        update_course_status(1, CourseStatus.NEW_DOWNLOADS_DISABLED)

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

    def test_can_edit_gamification_read_only_course(self):
        update_course_status(1, CourseStatus.READ_ONLY)

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)
