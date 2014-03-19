

import django.db.models
import json
from oppia.models import Tracker

def run():
    trackers = Tracker.objects.all()
    
    for t in trackers:
        try:
            json_data = json.loads(t.data)
            if json_data['lang']:
                t.lang = json_data['lang']
                t.save()
                print "saved: " + t.lang
        except:
            pass
                
if __name__ == "__main__":
    run()  