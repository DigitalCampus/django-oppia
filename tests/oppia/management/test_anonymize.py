from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import IntegrityError

from io import StringIO

from oppia.models import Tracker
from oppia.test import OppiaTestCase

from profile.models import UserProfile


class AnonymizeTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']

    STR_NO_INPUT = '--noinput'

    def test_anonymize(self):
        out = StringIO()
        settings.DEBUG = True
        call_command('anonymize', self.STR_NO_INPUT, stdout=out)

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
        call_command('anonymize', self.STR_NO_INPUT, stdout=out)

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

    def test_anonymize_integrity_errors(self):
        # add user with exisiting username the same as the id for admin
        user = User()
        user.username = "user1"
        user.password = make_password("1234")
        user.save()

        out = StringIO()
        settings.DEBUG = True
        call_command('anonymize', self.STR_NO_INPUT, stdout=out)

        self.assertRaises(IntegrityError)
        self.assertRaises(UserProfile.DoesNotExist)
        settings.DEBUG = False
