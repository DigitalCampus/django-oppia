'''
 Script to get user locations based on their IP address in the Tracker model
 
 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
'''

import time
import MySQLdb 
import urllib2 
import json 
import argparse, hashlib, subprocess
from django.db.models import Count
from oppia.models import Tracker
from oppia.viz.models import UserLocationVisualization

def run():
  
    tracker_ip_hits = Tracker.objects.filter(user__is_staff=False).values('ip').annotate(count_hits=Count('ip'))
    
    for t in tracker_ip_hits:
        # lookup whether already cached in db
        try:
            cached = UserLocationVisualization.objects.get(ip=t['ip'])
            cached.hits = t['count_hits']
            cached.save()
            print "hits updated"
        except UserLocationVisualization.DoesNotExist:
            update_via_freegeoip(t)

def update_via_freegeoip(t):
    url = 'https://freegeoip.net/json/%s' % (t['ip'])
    print t['ip'] + " : "+ url
    try:
        u = urllib2.urlopen(urllib2.Request(url), timeout=10)
        data = u.read()  
        dataJSON = json.loads(data,"utf-8")
        print dataJSON
    except:
        return
    
    try:
        if dataJSON['latitude'] != 0 and dataJSON['longitude'] != 0:
            viz = UserLocationVisualization()
            viz.ip = t['ip']
            viz.lat = dataJSON['latitude']
            viz.lng = dataJSON['longitude']
            viz.hits = t['count_hits']
            viz.region = dataJSON['city'] + " " + dataJSON['region_name'] 
            viz.country_code = dataJSON['country_code']
            viz.country_name = dataJSON['country_name']
            viz.geonames_data = dataJSON
            viz.save()
    except:
        pass
    time.sleep(1) 
                                         

if __name__ == "__main__":
    run()  
    
    
     