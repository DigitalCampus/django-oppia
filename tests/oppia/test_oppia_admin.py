import os
import shutil

import pytest
from django.conf import settings
from django.urls import reverse
from oppia.test import OppiaTestCase


class OppiaAdminTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_question_indices.json',
                'tests/awards/award-course.json',
                'tests/test_certificatetemplate.json']

    def test_course_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('admin:oppia_course_changelist'))
        self.assertEqual(200, response.status_code)

    def test_activity_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('admin:oppia_activity_changelist'))
        self.assertEqual(200, response.status_code)

    def test_certificate_preview(self):
        test_img_name = 'certificate_test2_aIeE1m6.png'
        src = os.path.join(settings.TEST_RESOURCES, 'certificate', 'templates', test_img_name)
        dst = os.path.join(settings.MEDIA_ROOT, 'certificate', 'templates', test_img_name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)

        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('oppia:certificate_preview',
                                           args={1}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(response['Content-Type'], "application/pdf")
