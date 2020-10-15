import datetime
import os
import time

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from oppia.management import commands
from oppia.models import Tracker

from settings.models import SettingProperties


class Command(BaseCommand):
    help = 'OppiaMobile data retention command'

    def add_arguments(self, parser):

        # Optional argument for years to start from
        parser.add_argument(
            '--years',
            dest='years',
            help='no years',
            type=int
        )
        
        parser.add_argument(
            '--noinput',
            dest='noinput',
            help='run without any user input'
        )
        
    def handle(self, *args, **options):
        if options['years']:
            years = options['years']
        else:
            years = 7
            
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
            
        last_login_date = datetime.datetime.now() - relativedelta(years=years)
        
        users_to_delete = []
        users = User.objects.filter(last_login__lte=last_login_date)
        
        for user in users:
            no_trackers = Tracker.objects.filter(
                user=user,
                submitted_date__gte=last_login_date).count()
            if no_trackers == 0:
                users_to_delete.append(user)
                
        if len(users_to_delete) > 0:
            print(_(u"The following users will be deleted:"))
            for user in users_to_delete:
                if not options['noinput']:
                    accept = input(_(u"Would you like to delete user %s? [y/n]" % user.username))
                    if accept == 'y':
                        User.objects.get(pk=user.id).delete() 
                else:
                    User.objects.get(pk=user.id).delete()          
        else:
            print(_(u"There are no users to remove"))
    