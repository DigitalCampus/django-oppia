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

def run(ip_key, geonames_user):
  
    tracker_ip_hits = Tracker.objects.filter(user__is_staff=False).values('ip').annotate(count_hits=Count('ip'))
    
    for t in tracker_ip_hits:
        # lookup whether already cached in db
        try:
            cached = UserLocationVisualization.objects.get(ip=t['ip'])
            cached.hits = t['count_hits']
            cached.save()
            print "hits updated"
        except UserLocationVisualization.DoesNotExist:
            url = 'http://api.ipaddresslabs.com/iplocation/v1.7/locateip?key=%s&ip=%s&format=json' % (ip_key, t['ip'])
            print t['ip'] + " : "+ url
            u = urllib2.urlopen(urllib2.Request(url))
            data = u.read()  
            dataJSON = json.loads(data)
            print dataJSON
            if 'geolocation_data' in dataJSON:
                print dataJSON['geolocation_data']
                url = 'http://api.geonames.org/searchJSON?username=%s&maxRows=1&q=%s&country=%s' % (geonames_user,dataJSON['geolocation_data']['region_name'],dataJSON['geolocation_data']['country_code_iso3166alpha2'])
                u = urllib2.urlopen(urllib2.Request(url))
                geo = u.read()  
                geoJSON = json.loads(geo)
                print geoJSON
                try:
                    viz = UserLocationVisualization()
                    viz.ip = t['ip']
                    viz.lat = geoJSON['geonames'][0]['lat']
                    viz.lng = geoJSON['geonames'][0]['lng']
                    viz.hits = t['count_hits']
                    viz.region = geoJSON['geonames'][0]['name']
                    viz.country_code = geoJSON['geonames'][0]['countryCode']
                    viz.country_name = geoJSON['geonames'][0]['countryName']
                    viz.geonames_data = geoJSON['geonames'][0]
                    viz.save()
                except UnicodeEncodeError:
                    pass
                except IndexError:
                    pass
                except KeyError:
                    pass
                time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_key", help="IP Address Labs API Key")
    parser.add_argument("geonames_user", help="Geonames username")
    args = parser.parse_args()
    run(args.ip_key, args.geonames_user)  
    
    
     