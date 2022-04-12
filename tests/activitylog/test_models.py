import os

from activitylog.models import UploadedActivityLog
from django.conf import settings
from django.urls import reverse
from oppia.test import OppiaTestCase
from pathlib import Path


class ActivityLogModelsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    activity_logs_folder = os.path.join(settings.TEST_RESOURCES, 'activity_logs')
    basic_activity_log = os.path.join(activity_logs_folder, 'basic_activity.json')
    url = reverse('activitylog:upload')

    def test_model_str(self):
        self.client.force_login(self.admin_user)

        with open(self.basic_activity_log, 'rb') as activity_log_file:
            self.client.post(self.url,
                             {'activity_log_file': activity_log_file})

        act_log = UploadedActivityLog.objects.latest('created_date')
        name_components = str(act_log).split('/')
        self.assertEqual(4, len(name_components))
        self.assertEqual('activitylog', name_components[0])

    def test_delete_file(self):
        self.client.force_login(self.admin_user)

        with open(self.basic_activity_log, 'rb') as activity_log_file:
            self.client.post(self.url,
                             {'activity_log_file': activity_log_file})

        act_log = UploadedActivityLog.objects.latest('created_date')
        path = Path(os.path.join(settings.MEDIA_ROOT, str(act_log)))
        self.assertTrue(path.exists())
        act_log.delete()
        self.assertFalse(path.exists())
