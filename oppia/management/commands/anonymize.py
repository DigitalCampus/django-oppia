import time

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _

from oppia.management import commands
from oppia.models import Tracker
from profile.models import UserProfile, UserProfileCustomField
from reports.models import DashboardAccessLog
from viz.models import UserLocationVisualization


class Command(BaseCommand):
    help = 'Script to anonymize an Oppia database'

    def add_arguments(self, parser):

        # Optional argument to start the summary calculation from the beginning
        parser.add_argument(
            '--noinput',
            dest='noinput',
            help='run without any user input',
        )

    def handle(self, *args, **options):
        print(commands.TERMINAL_COLOUR_WARNING)
        print(_(u"WARNING! This script will anonymize all non-admin and " +
                u"non-staff accounts, all users personal data, usernames, " +
                u"passwords etc will be removed"))
        print(commands.TERMINAL_COLOUR_ENDC)
        if not options['noinput']:
            accept = input(_(u" Without a backup you cannot recover from " +
                             u"this operation, are you sure you want to " +
                             u"continue? [y/n]"))
            if accept != 'y':
                print(_(u"Aborting"))
                return

        if not settings.DEBUG:
            print(commands.TERMINAL_COLOUR_WARNING)
            print(_(u"Your server is not in DEBUG mode, you can only apply " +
                    u"this script on an Oppia server in DEBUG mode"))
            print(_(u"Aborting"))
            print(commands.TERMINAL_COLOUR_ENDC)
            return

        users = User.objects.all()
        for u in users:
            print(_(u"Anonymizing id: {id}").format(id=u.id))

            # check if admin or staff user
            if u.is_superuser or u.is_staff:
                print(commands.TERMINAL_COLOUR_WARNING)
                print(_(u"{id} is an admin or staff user, they will not be " +
                        u"anonymised").format(id=u.id))
                print(commands.TERMINAL_COLOUR_ENDC)
                continue

            # user
            u.username = "user" + str(u.id)
            u.first_name = "User"
            u.last_name = u.id
            u.email = "user" + str(u.id) + "@oppia-mobile.org"
            u.password = make_password(time.time())
            try:
                u.save()
            except IntegrityError:
                u.username = "user" + str(time.time())
                u.save()

            # userprofile
            try:
                profile = UserProfile.objects.get(user=u)
                profile.about = ''
                profile.job_title = 'my job'
                profile.organisation = 'my organisation'
                profile.phone_no = '0123456789'
                profile.save()
            except UserProfile.DoesNotExist:
                pass

            # user custom profile field
            custom_user_fields = UserProfileCustomField.objects.filter(user=u)
            for cuf in custom_user_fields:
                cuf.delete()

            print(commands.TERMINAL_COLOUR_OK)
            print(_(u"Anonymized id: {id}").format(id=u.id))
            print(commands.TERMINAL_COLOUR_ENDC)

        # Dashboard access logs
        print(_(u"Anonymizing dashboard access logs"))
        DashboardAccessLog.objects.all().update(ip='127.0.0.1')
        DashboardAccessLog.objects.all().update(agent='my browser agent')
        DashboardAccessLog.objects.all().update(data='')

        print(commands.TERMINAL_COLOUR_OK)
        print(_(u"Dashboard access logs anonymized"))
        print(commands.TERMINAL_COLOUR_ENDC)

        # tracker
        print(_(u"Anonymizing trackers"))
        Tracker.objects.all().update(ip='127.0.0.1')
        Tracker.objects.all().update(agent='my browser agent')
        Tracker.objects.all().update(data='')
        print(commands.TERMINAL_COLOUR_OK)
        print(_(u"Trackers anonymized"))
        print(commands.TERMINAL_COLOUR_ENDC)

        # user location vizualizations
        print(_(u"Anonymizing user location vizualisations"))
        UserLocationVisualization.objects.all().delete()
        print(commands.TERMINAL_COLOUR_OK)
        print(_(u"User location vizualisations anonymized"))
        print(commands.TERMINAL_COLOUR_ENDC)

        # complete
        print(commands.TERMINAL_COLOUR_OK)
        print(_(u"Anonymization complete"))
        print(commands.TERMINAL_COLOUR_ENDC)
