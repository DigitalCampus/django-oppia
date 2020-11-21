# coding: utf-8
"""
Management command to get user locations based on their IP address in the
Tracker model
"""
import urllib
import json
import time

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from oppia.models import Tracker
from viz.models import UserLocationVisualization
from settings.models import SettingProperties
from settings import constants


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
                self.update_via_ipstack(t)

        self.stdout.write("completed")

    def update_via_ipstack(self, t):
        key = SettingProperties.get_string(constants.OPPIA_IPSTACK_APIKEY, '')

        if t['ip'] == '' or t['ip'] == None or key == '':
            return

        url = 'http://api.ipstack.com/%s?access_key=%s' % (t['ip'], key)
        self.stdout.write(t['ip'] + " : " + url)

        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            data_json = json.loads(data)

        if data_json['latitude'] != 0 and data_json['longitude'] != 0:
            viz = UserLocationVisualization()
            viz.ip = t['ip']
            viz.lat = data_json['latitude']
            viz.lng = data_json['longitude']
            viz.hits = t['count_hits']
            if 'city' in data_json and 'region_name' in data_json:
                viz.region = data_json['city'] + " " + data_json['region_name']
            elif 'city' in data_json:
                viz.region = data_json['city']
            elif 'region_name' in data_json:
                viz.region = data_json['region_name']
            viz.country_code = data_json['country_code']
            viz.country_name = data_json['country_name']
            viz.save()

        time.sleep(5)
