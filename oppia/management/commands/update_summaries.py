from distutils.util import strtobool

from django.core.management.base import BaseCommand
from oppia.summary.cron import run as summary_cron


class Command(BaseCommand):
    help = 'Updates course and points summary tables'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        summary_cron()
