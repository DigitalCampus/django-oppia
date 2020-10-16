from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command

from io import StringIO

from oppia.models import Tracker
from oppia.test import OppiaTestCase


class DataRetentionTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    STR_NO_INPUT = '--noinput'

    def test_data_retention_no_delete(self):
        out = StringIO()
        
        start_user_count = User.objects.all().count()
        call_command('data_retention', self.STR_NO_INPUT, stdout=out)
        end_user_count = User.objects.all().count()
        self.assertEqual(start_user_count, end_user_count)

    def test_data_retention_old_user(self):
        out = StringIO()
        user = User()
        user.username="olduser"
        user.last_login="2000-01-01"
        user.save()
        
        start_user_count = User.objects.all().count()
        call_command('data_retention', self.STR_NO_INPUT, stdout=out)
        end_user_count = User.objects.all().count()
        self.assertEqual(start_user_count-1, end_user_count)

    def test_data_retention_old_user_new_tracker(self):
        out = StringIO()
        user = User()
        user.username="olduser"
        user.last_login="2000-01-01"
        user.save()
        
        tracker = Tracker()
        tracker.user = user
        tracker.save()
        
        start_user_count = User.objects.all().count()
        call_command('data_retention', self.STR_NO_INPUT, stdout=out)
        end_user_count = User.objects.all().count()
        self.assertEqual(start_user_count, end_user_count)
