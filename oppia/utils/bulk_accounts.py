'''
 Script to create bulk user accounts
 
 
 format for input file:
 username, firstname, lastname, email, password, organisation, jobtitle
 
 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
'''

import argparse
import csv
import json
import urllib2

def run(url, file_name): 
    
    
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 7:
                print "Invalid no fields"
                continue
            else:
                username = row[0]
                firstname = row[1]
                lastname = row[2]
                email = row[3]
                password = row[4]
                organisation = row[5]
                jobtitle = row[6]
        
                payload = json.dumps({'username': username, 'firstname': firstname, 'lastname': lastname, 'email': email, 'password':password, 'passwordagain':password, 'jobtitle':jobtitle, 'organisation': organisation})
                clen = len(payload)
                req = urllib2.Request(url, payload, {'Content-Type': 'application/json', 'Content-Length': clen, 'Accept': 'application/json'})
                
                try:
                    f = urllib2.urlopen(req)
                    json_response = json.loads(f.read())
                    f.close()
                    print username + ": account created"
                except urllib2.HTTPError:
                    print username + ": account NOT created"

    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server", help="e.g. http://localhost:8000/api/v1/register/")
    parser.add_argument("file_name", help="")
    args = parser.parse_args()
    run(args.server, args.file_name)  