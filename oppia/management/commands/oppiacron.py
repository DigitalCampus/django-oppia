from django.core.management.base import BaseCommand

from settings.models import SettingProperties
from oppia.cron import oppia_cron


class Command(BaseCommand):
    help = 'OppiaMobile '

    def add_arguments(self, parser):

        # Optional argument to start the summary calculation from the beginning
        parser.add_argument(
            '--hours',
            dest='hours',
            help='no hours',
        )

    def handle(self, *args, **options):
        if options['hours']:
            oppia_cron(options['hours'])
        else:
            oppia_cron(0) 