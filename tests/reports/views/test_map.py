
from oppia.test import OppiaTestCase
from django.urls import reverse

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

    url = reverse('reports:map')

    # map
    def test_view_map_disabled(self):
        SettingProperties.set_bool(
            constants.OPPIA_MAP_VISUALISATION_ENABLED,
            False)

        allowed_users = [self.admin_user,
                         self.staff_user]

        disallowed_users = [self.teacher_user,
                            self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(self.url)
            self.assertEqual(404, response.status_code)

        for disallowed_user in disallowed_users:
            self.client.force_login(disallowed_user)
            response = self.client.get(self.url)
            self.assertEqual(302, response.status_code)

    def test_view_map_enabled(self):
        SettingProperties.set_bool(
            constants.OPPIA_MAP_VISUALISATION_ENABLED,
            True)

        allowed_users = [self.admin_user,
                         self.staff_user]

        disallowed_users = [self.teacher_user,
                            self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, 'reports/map.html')
            self.assertEqual(200, response.status_code)

        for disallowed_user in disallowed_users:
            self.client.force_login(disallowed_user)
            response = self.client.get(self.url)
            self.assertEqual(302, response.status_code)
