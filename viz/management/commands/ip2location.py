# coding: utf-8
"""
Management command to get user locations based on their IP address in the Tracker model
"""

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from oppia.models import Tracker
from viz import UserLocationVisualization


class Command(BaseCommand):
    help = _(u'Gets user locations based on their IP address in the Tracker model')

    def handle(self, *args, **options):
        tracker_ip_hits = Tracker.objects.filter(user__is_staff=False).values('ip').annotate(count_hits=Count('ip'))

        for t in tracker_ip_hits:
            # lookup whether already cached in db
            try:
                cached = UserLocationVisualization.objects.get(ip=t['ip'])
                cached.hits = t['count_hits']
                cached.save()
                print("hits updated")
            except UserLocationVisualization.DoesNotExist:
                update_via_freegeoip(t)


def update_via_freegeoip(t):
    url = 'https://freegeoip.net/json/%s' % (t['ip'])
    print(t['ip'] + " : " + url)
    try:
        u = urllib2.urlopen(urllib2.Request(url), timeout=10)
        data = u.read()
        data_json = json.loads(data, "utf-8")
        print(data_json)
    except:
        return

    if data_json['latitude'] != 0 and data_json['longitude'] != 0:
        viz = UserLocationVisualization()
        viz.ip = t['ip']
        viz.lat = data_json['latitude']
        viz.lng = data_json['longitude']
        viz.hits = t['count_hits']
        viz.region = data_json['city'] + " " + data_json['region_name']
        viz.country_code = data_json['country_code']
        viz.country_name = data_json['country_name']
        viz.geonames_data = data_json
        viz.save()

    time.sleep(commands.DEFAULT_SLEEP)
