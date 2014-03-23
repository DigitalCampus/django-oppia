'''
 Checks the media download urls to ensure they are valid links
 
 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
'''

import urllib2
import time 
import django.db.models
from django.conf import settings
from oppia.models import Media

def run():
    media = Media.objects.all()
    for m in media:
        print "Checking: " + m.filename
        try:
            req = urllib2.Request(m.download_url)
            response = urllib2.urlopen(req)
            if m.filesize is not None:
                total_size = int(response.headers['content-length'])
                if total_size != m.filesize:
                    print "INFO: file sizes appear to be different:"
                    print "filesize recorded in db:" + m.filesize
                    print "filesize of download url:" + total_size
        except urllib2.HTTPError:
            print "WARNING: media file not found at: "+ m.download_url
                
if __name__ == "__main__":
    run()  