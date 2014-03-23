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

from django.db.models import Sum

from oppia.viz.models import UserLocationVisualization


def run(cartodb_account, cartodb_key): 
    
    cartodb_table = "oppiamobile_users" 
    
    # check can connect to cartodb API
    sql = "SELECT count(*) FROM %s" % (cartodb_table)
    url = "http://%s.cartodb.com/api/v2/sql?q=%s" % (cartodb_account,sql)
    u = urllib.urlopen(url)
    data = u.read() 
    dataJSON = json.loads(data)

    locations = UserLocationVisualization.objects.values('lat','lng').annotate(total_hits=Sum('hits'))
    for l in locations :
        
        # find if already in cartodb
        sql = "SELECT * FROM %s WHERE lat=%f AND lng=%f" % (cartodb_table,l['lat'],l['lng'])
        url = "http://%s.cartodb.com/api/v2/sql?q=%s" % (cartodb_account,sql)
        u = urllib.urlopen(url)
        data = u.read() 
        dataJSON = json.loads(data)
        #print dataJSON
        
        # if found then update total hits
        if dataJSON['total_rows'] == 1:
            # only need to update if the no total_hits is different to before
            no_hits = dataJSON['rows'][0]['total_hits']
            if l['total_hits'] != no_hits:
                print "found - will update"
                cartodb_id = dataJSON['rows'][0]['cartodb_id']
                print cartodb_id
                sql = "UPDATE %s SET total_hits=%d WHERE cartodb_id=%d" % (cartodb_table,l['total_hits'], cartodb_id)
                url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account,sql,cartodb_key)
                u = urllib.urlopen(url)
                data = u.read() 
                dataJSON = json.loads(data)
                print dataJSON
               
            else:
                print "row already up to date"
        else:
        # if not found then insert
            print "not found - will insert"
            sql = "INSERT INTO %s (the_geom, lat, lng, total_hits) VALUES (ST_SetSRID(ST_Point(%f, %f),4326),%f,%f,%d)" % (cartodb_table,l['lng'],l['lat'],l['lat'],l['lng'],l['total_hits'])
            url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account,sql,cartodb_key)
            u = urllib.urlopen(url)
            data = u.read() 
            dataJSON = json.loads(data)
            print dataJSON
            
         # pause for a bit
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cartodb_account", help="CartoDB Account Name")
    parser.add_argument("cartodb_key", help="CartoDB API Key")
    #parser.add_argument("cartodb_table", help="CartoDB table name")
    args = parser.parse_args()
    run(args.cartodb_account, args.cartodb_key)  
    
    
    
    