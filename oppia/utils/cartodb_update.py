# /usr/bin/env python

import time
import MySQLdb 
import urllib 
import json 
import argparse, hashlib, subprocess


def run(db_user, db_password, database, cartodb_account, cartodb_key): 
    
    cartodb_table = "dbip_cache_live"
    
    ipdb = MySQLdb.connect(host="localhost", # your host, usually localhost
                         user=db_user, # your username
                          passwd=db_password, # your password
                          db=database) # name of the data base
    ipdbcur = ipdb.cursor() 
    
    # check can connect to cartodb API
    url = "http://"+ cartodb_account+".cartodb.com/api/v2/sql?q=SELECT count(*) FROM " + cartodb_table
    u = urllib.urlopen(url)
    data = u.read() 
    dataJSON = json.loads(data)
    #print dataJSON

    ipdbcur.execute("SELECT lat, lng, sum(hits) as total_hits FROM dbip_cache GROUP BY lat,lng")
    for row in ipdbcur.fetchall() :
        
        # find if already in cartodb
        sql = "SELECT * FROM %s WHERE lat=%f AND lng=%f" % (cartodb_table,row[0],row[1])
        url = "http://%s.cartodb.com/api/v2/sql?q=%s" % (cartodb_account,sql)
        u = urllib.urlopen(url)
        data = u.read() 
        dataJSON = json.loads(data)
        #print dataJSON
        
        # if found then update total hits
        if dataJSON['total_rows'] == 1:
            # only need to update if the no total_hits is different to before
            no_hits = dataJSON['rows'][0]['total_hits']
            if row[2] != no_hits:
                print "found - will update"
                cartodb_id = dataJSON['rows'][0]['cartodb_id']
                print cartodb_id
                sql = "UPDATE %s SET total_hits=%d WHERE cartodb_id=%d" % (cartodb_table,row[2], cartodb_id)
                url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account,sql,cartodb_key)
                u = urllib.urlopen(url)
                data = u.read() 
                dataJSON = json.loads(data)
                print dataJSON
                # pause for few seconds
                time.sleep(3)
            else:
                print "row already up to date"
        else:
        # if not found then insert
            print "not found - will insert"
            sql = "INSERT INTO %s (lat,lng,total_hits) VALUES (%f,%f,%d)" % (cartodb_table,row[0],row[1],row[2])
            url = "http://%s.cartodb.com/api/v2/sql?q=%s&api_key=%s" % (cartodb_account,sql,cartodb_key)
            u = urllib.urlopen(url)
            data = u.read() 
            dataJSON = json.loads(data)
            print dataJSON
            # pause for few seconds
            time.sleep(3)
        
    ipdbcur.close()
    ipdb.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="database username")
    parser.add_argument("password", help="database password")
    parser.add_argument("database", help="database name")
    parser.add_argument("cartodb_account", help="CartoDB Account Name")
    parser.add_argument("cartodb_key", help="CartoDB API Key")
    args = parser.parse_args()
    run(args.username, args.password, args.database, args.cartodb_account, args.cartodb_key)  
    
    
    
    