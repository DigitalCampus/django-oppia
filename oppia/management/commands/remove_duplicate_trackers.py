# coding: utf-8

"""
Management command to remove any duplicate trackers (based on UUID)
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Count, Min, Q
from django.utils.translation import ugettext_lazy as _

from oppia.models import Tracker


class Command(BaseCommand):
    help = _(u"Removes any duplicate trackers based on UUID")

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Remove page/media/quiz trackers with no UUID
        """
        result = Tracker.objects.filter(Q(type='page') | Q(type='quiz') | Q(type='media'), uuid=None).delete()
        print(_(u"\n\n%d trackers removed that had no UUID\n" % result[0]))

        """
        Remove proper duplicate trackers - using min id
        """
        trackers = Tracker.objects.filter(Q(type='page') | Q(type='quiz') | Q(type='media')).values('uuid').annotate(dcount=Count('uuid')).filter(dcount__gte=2)

        for index, tracker in enumerate(trackers):
            print("%d/%d" % (index, trackers.count()))
            exclude = Tracker.objects.filter(uuid=tracker['uuid']).aggregate(min_id=Min('id'))
            deleted = Tracker.objects.filter(uuid=tracker['uuid']).exclude(id=exclude['min_id']).delete()
            print(_(u"%d duplicate tracker(s) removed for UUID %s based on min id" % (deleted[0], tracker['uuid'])))
            
        """
        Remember to run summary cron from start
        """
        if result[0] + trackers.count() > 0:
            print(_(u"Since duplicates have been found and removed, you should now run `update_summaries` to ensure the dashboard graphs are accurate."))
            accept = raw_input(_(u"Would you like to run `update_summaries` now? [Yes/No]"))
            if accept == 'y':
                call_command('update_summaries', fromstart=True)
