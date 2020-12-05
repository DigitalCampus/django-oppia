from django.urls import reverse

from oppia.test import OppiaTestCase
from oppia.models import Tracker

class AwardsTestCase(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json']
    file_root = './oppia/fixtures/tests/awards/'
    url = reverse('activitylog:upload')
    
    def load_data_helper(self, file):
        tracker_file = self.file_root + file
        self.client.force_login(self.admin_user)
    
        tracker_count_start = Tracker.objects.all().count()
        with open(tracker_file, 'rb') as file:
            self.client.post(self.url, {'activity_log_file': file})
        
        return tracker_count_start