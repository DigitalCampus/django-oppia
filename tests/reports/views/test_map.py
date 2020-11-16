import datetime

from oppia.test import OppiaTestCase
from django.urls import reverse
from django.utils import timezone

from settings import constants
from settings.models import SettingProperties


class MapViewTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_viz.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_course_permissions.json']

    # map
    def test_view_map_disabled(self):
        SettingProperties.set_bool(
            constants.OPPIA_MAP_VISUALISATION_ENABLED,
            False)

        allowed_users = [self.admin_user,
                         self.teacher_user,
                         self.staff_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(reverse('reports:map'))
            self.assertEqual(404, response.status_code)

    def test_view_map_enabled(self):
        SettingProperties.set_bool(
            constants.OPPIA_MAP_VISUALISATION_ENABLED,
            True)

        allowed_users = [self.admin_user,
                         self.teacher_user,
                         self.staff_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(reverse('reports:map'))
            self.assertTemplateUsed(response, 'report/map.html')
            self.assertEqual(response.status_code, 200)