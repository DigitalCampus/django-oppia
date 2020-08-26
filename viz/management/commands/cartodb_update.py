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

from urllib.parse import urlencode, quote_plus

from viz.models import UserLocationVisualization

CARTODB_TABLE = "oppiamobile_users"


class Command(BaseCommand):
    help = 'Updates user map on CartoDB'

    CARTO_DB_QUERY = "https://%s.cartodb.com/api/v2/sql?%s"

    def handle(self, *args, **options):
        cartodb_account = SettingProperties \
            .get_string(constants.OPPIA_CARTODB_ACCOUNT, None)
        cartodb_key = SettingProperties \
            .get_string(constants.OPPIA_CARTODB_KEY, None)
        source_site = SettingProperties \
            .get_string(constants.OPPIA_HOSTNAME, None)

        print(cartodb_account)
        print(cartodb_key)
        print(source_site)

        if cartodb_account is None \
                or cartodb_key is None \
                or source_site is None:
            self.stdout.write("Please check account/key and source site.")
            return

        # check can connect to cartodb API
        payload = {'q': "SELECT * FROM %s WHERE source_site='%s'"
                   % (CARTODB_TABLE, source_site)}
        url = self.CARTO_DB_QUERY % (cartodb_account,
                                     urlencode(payload, quote_via=quote_plus))
        u = urllib.request.urlopen(url)
        data = u.read()
        carto_db_data = json.loads(data)

        # update any existing points
        for c in carto_db_data['rows']:
            location = UserLocationVisualization.objects \
                .filter(lat=c['lat'],
                        lng=c['lng']).aggregate(total=Sum('hits'))
            if location['total'] is not None \
                    and c['total_hits'] != location['total']:
                self.stdout.write("found - will update")
                cartodb_id = c['cartodb_id']
                payload = {'q': "UPDATE %s SET total_hits=%d WHERE cartodb_id=%d  \
                      AND source_site='%s'" % (CARTODB_TABLE,
                                               location['total'],
                                               cartodb_id,
                                               source_site),
                           'api_key': cartodb_key}

                url = self.CARTO_DB_QUERY \
                    % (cartodb_account,
                       urlencode(payload, quote_via=quote_plus))
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    data = response.read()

                    data_json = json.loads(data)
                    print(data_json)
                time.sleep(1)

        # add any new points
        locations = UserLocationVisualization.objects \
            .exclude(lat=0, lng=0) \
            .values('lat', 'lng', 'country_code') \
            .annotate(total_hits=Sum('hits'))
        for location in locations:
            found = False
            # loop through and see if in carto_db_data
            for c in carto_db_data['rows']:
                if location['lat'] == c['lat'] and location['lng'] == c['lng']:
                    found = True

            if not found:
                self.stdout.write("not found - will insert")
                sql_str = "INSERT INTO %s (the_geom, lat, lng, total_hits, \
                        country_code, source_site) VALUES \
                        (ST_SetSRID(ST_Point(%f, %f),4326), \
                        %f,%f,%d ,'%s','%s')"
                sql = sql_str % \
                    (CARTODB_TABLE,
                     location['lng'],
                     location['lat'],
                     location['lat'],
                     location['lng'],
                     location['total_hits'],
                     location['country_code'],
                     source_site)
                payload = {'q': sql, 'api_key': cartodb_key}

                url = self.CARTO_DB_QUERY % \
                    (cartodb_account,
                     urlencode(payload, quote_via=quote_plus))
                u = urllib.request.urlopen(url)
                data = u.read()
                print(data)
                time.sleep(1)
