from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER


class OppiaTestCase(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_malaria_quiz.json',
                'tests/test_av_uploadedmedia.json',
                'tests/test_viz.json']

    def setUp(self):
        super(OppiaTestCase, self).setUp()
        
        self.login_url = reverse('profile_login')
        
        self.admin_user = User.objects.get(pk=ADMIN_USER['id'])
        self.staff_user = User.objects.get(pk=STAFF_USER['id'])
        self.teacher_user = User.objects.get(pk=TEACHER_USER['id'])
        self.normal_user = User.objects.get(pk=NORMAL_USER['id'])

    
    def get_view(self, route, user=None):
        if user is not None:
            self.client.force_login(user)
        return self.client.get(route)