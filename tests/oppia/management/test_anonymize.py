from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from oppia.test import OppiaTestCase
from io import StringIO
from oppia.models import Tracker


class AnonymizeTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_permissions.json',
                'default_badges.json']

    def test_anonymize(self):
        out = StringIO()
        settings.DEBUG = True
        call_command('anonymize', '--noinput=True', stdout=out)

        # username admin
        user = User.objects.get(pk=self.admin_user.pk)
        self.assertEqual('admin', user.username)

        # username staff
        user = User.objects.get(pk=self.staff_user.pk)
        self.assertEqual('staff', user.username)

        # username teacher
        user = User.objects.get(pk=self.teacher_user.pk)
        self.assertEqual('user4', user.username)

        # username normaluser
        user = User.objects.get(pk=self.normal_user.pk)
        self.assertEqual('user2', user.username)

        # trackers
        trackers = Tracker.objects.all().exclude(ip='127.0.0.1')
        self.assertEqual(0, trackers.count())

        settings.DEBUG = False

    def test_anonymize_not_debug(self):
        out = StringIO()
        settings.DEBUG = False
        call_command('anonymize', '--noinput=True', stdout=out)

        # username admin
        user = User.objects.get(pk=self.admin_user.pk)
        self.assertEqual('admin', user.username)

        # username staff
        user = User.objects.get(pk=self.staff_user.pk)
        self.assertEqual('staff', user.username)

        # username teacher
        user = User.objects.get(pk=self.teacher_user.pk)
        self.assertEqual('teacher', user.username)

        # username normaluser
        user = User.objects.get(pk=self.normal_user.pk)
        self.assertEqual('demo', user.username)
