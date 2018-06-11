
import oppia.management.commands

from distutils.util import strtobool

from django.core.management.base import BaseCommand

from oppia.settings.models import SettingProperties
from oppia.summary.cron import update_summaries

class Command(BaseCommand):
    help = 'Updates course and points summary tables'

    def add_arguments(self, parser):

        # Optional argument to start the summary calculation from the beginning
        parser.add_argument(
            '--fromstart',
            action='store_true',
            dest='fromstart',
            help='Calculate summary tables from the beginning, not just the last ones',
        )

    def handle(self, *args, **options):
        if options['fromstart']:
            update_summaries(0, 0)
        else:
            # get last tracker and points PKs processed
            last_tracker_pk = SettingProperties.get_property('last_tracker_pk', 0)
            last_points_pk = SettingProperties.get_property('last_points_pk', 0)
            update_summaries(last_tracker_pk, last_points_pk)
