# coding: utf-8
"""
Management command to get user locations based on their IP address in the
Tracker model
"""

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from oppia.models import Tracker
from viz.models import UserLocationVisualization


class Command(BaseCommand):
    help = _(u'Gets user locations based on their IP address in the \
            Tracker model')

    def handle(self, *args, **options):
        tracker_ip_hits = Tracker.objects \
            .filter(user__is_staff=False) \
            .values('ip') \
            .annotate(count_hits=Count('ip'))

        for t in tracker_ip_hits:
            # lookup whether already cached in db
            try:
                cached = UserLocationVisualization.objects.get(ip=t['ip'])
                cached.hits = t['count_hits']
                cached.save()
                self.stdout.write("hits updated")
            except UserLocationVisualization.DoesNotExist:
                pass
                # https://freegeoip.net is no longer available
                # see: issue:
                # https://github.com/DigitalCampus/django-oppia/issues/720

        self.stdout.write("completed")
