# coding: utf-8
"""
Management command to user map on CartoDB
"""
import json
import time
import urllib

from django.core.management.base import BaseCommand
from django.db.models import Sum

from settings.models import SettingProperties
from settings import constants

from viz.models import UserLocationVisualization

CARTODB_TABLE = "oppiamobile_users"


class Command(BaseCommand):
    help = 'Updates user map on CartoDB'

    def handle(self, *args, **options):
        cartodb_account = SettingProperties.get_string(constants.OPPIA_CARBODB_ACCOUNT, None)
        cartodb_key = SettingProperties.get_string(constants.OPPIA_CARBODB_KEY, None)
        source_site = SettingProperties.get_string(constants.OPPIA_HOSTNAME, None)

        # check can connect to cartodb API
        sql = "SELECT * FROM %s WHERE source_site='%s'" % (CARTODB_TABLE, source_site)
        url = "http://%s.cartodb.com/api/v2/sql?q=%s" % (cartodb_account, sql)
        u = urllib.urlopen(url)
        data = u.read()
        carto_db_data = json.loads(data)

        # update any existing points
        for c in carto_db_data['rows']:
            location = UserLocationVisualization.objects.filter(lat=c['lat'], lng=c['lng']).aggregate(total=Sum('hits'))
            if location['total'] != None and c['total_hits'] != location['total']:
                self.stdout.write("found - will update")
                cartodb_id = c['cartodb_id']
                sql = "UPDATE %s SET total_hits=%d WHERE cartodb_id=%d AND source_site='%s'" % (CARTODB_TABLE, location['total'], cartodb_id, source_site)
                url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account, sql, cartodb_key)
                u = urllib.urlopen(url)
                data = u.read()
                data_json = json.loads(data)
                self.stdout.write(data_json)
                time.sleep(1)

        # add any new points
        locations = UserLocationVisualization.objects.exclude(lat=0, lng=0).values('lat', 'lng', 'country_code').annotate(total_hits=Sum('hits'))
        for l in locations:
            found = False
            # loop through and see if in carto_db_data
            for c in carto_db_data['rows']:
                if l['lat'] == c['lat'] and l['lng'] == c['lng']:
                    found = True

            if not found:
                self.stdout.write("not found - will insert")
                sql = "INSERT INTO %s (the_geom, lat, lng, total_hits, country_code, source_site) VALUES (ST_SetSRID(ST_Point(%f, %f),4326),%f,%f,%d ,'%s','%s')" % (CARTODB_TABLE, l['lng'], l['lat'], l['lat'], l['lng'], l['total_hits'], l['country_code'], source_site)
                url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account, sql, cartodb_key)
                u = urllib.urlopen(url)
                data = u.read()
                data_json = json.loads(data)
                self.stdout.write(data)
                time.sleep(1)
