'''
 Script to update user map on CartoDB
 
 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
'''

import time
import MySQLdb 
import urllib
import json 
import argparse, hashlib, subprocess

from django.db.models import Sum, Q

from oppia.viz.models import UserLocationVisualization


def run(cartodb_account, cartodb_key, source_site): 
    
    cartodb_table = "oppiamobile_users" 
    
    # check can connect to cartodb API
    sql =  "SELECT * FROM %s WHERE source_site='%s'" % (cartodb_table, source_site)
    url = "http://%s.cartodb.com/api/v2/sql?q=%s" % (cartodb_account,sql)
    u = urllib.urlopen(url)
    data = u.read() 
    carto_db_data = json.loads(data)
    #print carto_db_data
    
   
    # update any existing points in the carto db
    for c in carto_db_data['rows']:
        location = UserLocationVisualization.objects.filter(lat = c['lat'], lng = c['lng']).aggregate(total=Sum('hits'))
        if location['total'] != None and c['total_hits'] != location['total']:
            # update
            print "found - will update"
            cartodb_id = c['cartodb_id']
            sql = "UPDATE %s SET total_hits=%d WHERE cartodb_id=%d AND source_site='%s'" % (cartodb_table,location['total'], cartodb_id, source_site)
            url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account,sql,cartodb_key)
            u = urllib.urlopen(url)
            data = u.read() 
            dataJSON = json.loads(data)
            print dataJSON
            time.sleep(1)
 
    # add any new points 
    locations = UserLocationVisualization.objects.exclude(lat=0, lng=0).values('lat','lng','country_code').annotate(total_hits=Sum('hits'))
    for l in locations:
        found = False
        # loop through and see if in carto_db_data
        for c in carto_db_data['rows']:
            if l['lat'] == c['lat'] and l['lng'] == c['lng']:
                found = True
                
        if not found:
            print "not found - will insert"
            sql = "INSERT INTO %s (the_geom, lat, lng, total_hits, country_code, source_site) VALUES (ST_SetSRID(ST_Point(%f, %f),4326),%f,%f,%d ,'%s','%s')" % (cartodb_table,l['lng'],l['lat'],l['lat'],l['lng'],l['total_hits'],l['country_code'], source_site)
            url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account,sql,cartodb_key)
            u = urllib.urlopen(url)
            data = u.read() 
            dataJSON = json.loads(data)
            print dataJSON
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cartodb_account", help="CartoDB Account Name")
    parser.add_argument("cartodb_key", help="CartoDB API Key")
    parser.add_argument("source_site", help="Source database")
    args = parser.parse_args()
    run(args.cartodb_account, args.cartodb_key, args.source_site)  
    
    
    
    