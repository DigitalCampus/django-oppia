# /usr/bin/env python

import time
import MySQLdb 
import urllib 
import json 
import argparse, hashlib, subprocess


def run(db_user, db_password, db_name, ip_key, geonames_user):
    oppiadb = MySQLdb.connect(host="localhost", # your host, usually localhost
                         user=db_user, # your username
                          passwd=db_password, # your password
                          db=db_name) # name of the data base
    oppiacur = oppiadb.cursor() 
    
    ipdb = MySQLdb.connect(host="localhost", # your host, usually localhost
                         user=db_user, # your username
                          passwd=db_password, # your password
                          db="ipdb") # name of the data base
    ipdbcur = ipdb.cursor() 
    
    # Use all the SQL you like
    oppiacur.execute("SELECT ip , count(*) as count_hits FROM oppia_tracker GROUP BY ip")
    
    print oppiacur.rowcount
    # print all the first cell of all the rows
    for row in oppiacur.fetchall() :
        # lookup whether already cached in db
        ipdbcur.execute("SELECT lat, lng FROM dbip_cache WHERE ip='" + row[0]+ "'")
        ver = ipdbcur.fetchone()
        if ipdbcur.rowcount == 0:
             # if not cached then call to Geonames db
            # and insert into cache
            url = 'http://api.ipaddresslabs.com/iplocation/v1.7/locateip?key='+ip_key+'&ip='+row[0]+'&format=json'
            #url = 'http://api.geonames.org/searchJSON?username=alexlittle&maxRows=1&q='+urllib.quote_plus(ipdbver[2])+'&country='+urllib.quote_plus(ipdbver[0])
            print row[0] + " : "+ url
            u = urllib.urlopen(url)
            data = u.read()  
            dataJSON = json.loads(data)
            print dataJSON
            if 'geolocation_data' in dataJSON:
                print dataJSON['geolocation_data']
                
                url = 'http://api.geonames.org/searchJSON?username='+geonames_user+'&maxRows=1&q='+urllib.quote_plus(dataJSON['geolocation_data']['region_name'])+'&country='+urllib.quote_plus(dataJSON['geolocation_data']['country_code_iso3166alpha2'])
                u = urllib.urlopen(url)
                geo = u.read()  
                geoJSON = json.loads(geo)
                print geoJSON
                try:
                    ipdbcur.execute("INSERT INTO dbip_cache (ip,lat,lng, hits, region, country) VALUES " +
                                    "('"+ row[0]+"',"+str(geoJSON['geonames'][0]['lat'])+","+str(geoJSON['geonames'][0]['lng']) +
                                    ","+str(row[1])+",%s,%s)",(geoJSON['geonames'][0]['name'],geoJSON['geonames'][0]['countryCode'],))
                    ipdb.commit()
                except UnicodeEncodeError:
                    pass
                except IndexError:
                    pass
                    
            time.sleep(3)
        else:
            #print "found in cache"
            ipdbcur.execute("UPDATE dbip_cache SET hits ="+str(row[1])+" WHERE ip='"+str(row[0])+"'")
            ipdb.commit()
            print "hits updated"
       
        #print row[0]
    oppiacur.close()
    ipdbcur.close()
    
    oppiadb.close()
    ipdb.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="database username")
    parser.add_argument("password", help="database password")
    parser.add_argument("database", help="database name")
    parser.add_argument("ip_key", help="IP Address Labs API Key")
    parser.add_argument("geonames_user", help="Geonames username")
    args = parser.parse_args()
    run(args.username, args.password, args.database, args.ip_key, args.geonames_user)  
    
    
     