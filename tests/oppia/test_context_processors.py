import json

from django.urls import reverse
from oppia.test import OppiaTestCase

from reports.models import DashboardAccessLog


class ContextProcessorTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_question_indices.json',
                'tests/awards/award-course.json',
                'tests/test_certificatetemplate.json']

    # home page not logged in
    def test_get_home_not_logged_in(self):
        dal_start_count = DashboardAccessLog.objects.all().count()
        self.client.get(reverse('oppia:index'))
        dal_end_count = DashboardAccessLog.objects.all().count()
        # shouldn't add a log for non logged in users
        self.assertEqual(dal_start_count, dal_end_count)

    # home page - all users - get
    def test_get_home_logged_in(self):
        for user in (self.admin_user,
                     self.normal_user,
                     self.teacher_user,
                     self.staff_user):
            self.client.force_login(user=user)
            dal_start_count = DashboardAccessLog.objects.all().count()
            self.client.get(reverse('oppia:index'), follow=True)
            dal_end_count = DashboardAccessLog.objects.all().count()
            self.assertEqual(dal_start_count+1, dal_end_count)

    # home page - all users - post
    def test_post_home_logged_in(self):
        for user in (self.admin_user,
                     self.normal_user,
                     self.teacher_user,
                     self.staff_user):
            self.client.force_login(user=user)
            dal_start_count = DashboardAccessLog.objects.all().count()
            self.client.post(reverse('oppia:index'),
                             follow=True,
                             data={'test':'mytest'})
            dal_end_count = DashboardAccessLog.objects.all().count()
            self.assertEqual(dal_start_count+1, dal_end_count)
            
    # admin pages get
    def test_get_admin(self):
        dal_start_count = DashboardAccessLog.objects.all().count()
        self.client.force_login(user=self.admin_user)
        self.client.get(reverse('admin:oppia_course_changelist'))
        dal_end_count = DashboardAccessLog.objects.all().count()
        # shouldn't add a log for admin
        self.assertEqual(dal_start_count, dal_end_count)
    
    # admin pages post
    
    # api pages
    
    # sensitive info