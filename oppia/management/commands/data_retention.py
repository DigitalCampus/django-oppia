import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from oppia.management import commands
from oppia.models import Tracker

from settings.models import SettingProperties
from settings import constants


class Command(BaseCommand):
    help = 'OppiaMobile data retention command'

    def add_arguments(self, parser):

        parser.add_argument(
            '--noinput',
            action='store_true',
            dest='noinput',
            help='run without any user input'
        )

    def handle(self, *args, **options):
        years = SettingProperties.get_property(
            constants.OPPIA_DATA_RETENTION_YEARS, 999)

        print(commands.TERMINAL_COLOUR_WARNING)
        print(_(u"WARNING! This script will delete any user profiles and " +
                u"tracker data for users who have not logged in or had any " +
                u"tracker logs recorded for the last %d years") % years)
        print(commands.TERMINAL_COLOUR_ENDC)
        if not options['noinput']:
            accept = input(_(u"Would you like to continue? [y/n]"))
            if accept != 'y':
                print(_(u"Aborting"))
                return

        users_to_delete = self.get_users_to_delete(years)
        users_removed = 0
        if len(users_to_delete) > 0:
            users_removed = self.delete_users(options, users_to_delete)
        else:
            print(_(u"There are no users to remove"))

        if users_removed > 0:
            self.run_summaries(options)

    def get_users_to_delete(self, years):
        last_login_date = datetime.datetime.now() - relativedelta(years=years)

        users_to_delete = []
        users = User.objects.filter(last_login__lte=last_login_date)

        for user in users:
            no_trackers = Tracker.objects.filter(
                user=user,
                submitted_date__gte=last_login_date).count()
            if no_trackers == 0:
                users_to_delete.append(user)

        return users_to_delete

    def delete_users(self, options, users_to_delete):
        users_removed = 0
        print(_(u"The following users will be deleted:"))
        for user in users_to_delete:
            if not options['noinput']:
                accept = input(_(u"Would you like to delete user %s? [y/n]"
                                 % user.username))
                if accept == 'y':
                    print(_(u"User %s deleted" % user.username))
                    User.objects.get(pk=user.id).delete()
                    users_removed += 1
            else:
                print(_(u"User %s deleted" % user.username))
                User.objects.get(pk=user.id).delete()
                users_removed += 1
        return users_removed

    def run_summaries(self, options):
        if not options['noinput']:
            accept = input(_(u"Since users have been removed. Would you " +
                             u"to run `update_summaries` now? [y/n]"))
            if accept == 'y':
                call_command('update_summaries', fromstart=True)
        else:
            print(_(u"Now running the update_summaries task"))
            call_command('update_summaries', fromstart=True)
