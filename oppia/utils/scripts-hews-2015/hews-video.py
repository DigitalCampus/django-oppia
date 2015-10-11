import json
import datetime
from codecs import open

def run(): 
    
    from django.contrib.auth.models import User
    from django.db.models import Sum, Max, Min, Avg
    from django.utils.html import strip_tags
    
    from oppia.models import Activity, Course, Cohort, CourseCohort, Participant, Tracker, Media
    
    cohort_id = 23
    
    students = User.objects.filter(participant__cohort_id=cohort_id, participant__role=Participant.STUDENT).order_by('username')
    courses = Course.objects.filter(coursecohort__cohort__pk=cohort_id)
    
    trackers = Tracker.objects.filter(user__in=students,course__in=courses, type=Activity.MEDIA)
    
    print trackers.count()
    
    video_views = []
    
    for tracker in trackers:
        data = json.loads(tracker.data)
        found = False
        
        if tracker.time_taken < 0:
            continue
         
        media = Media.objects.filter(digest = tracker.digest)[:1]
        if media[0].media_length is None:
            print "NONE?!" + media[0].filename
            
        max_time = media[0].media_length
           
        for vv in video_views:
            if vv['mediafile'] == data['mediafile']:
                vv['users'].append(tracker.user.id)
                if tracker.time_taken > max_time:
                    vv['time_taken'] += max_time
                else:
                    vv['time_taken'] += tracker.time_taken
                vv['uuid'].append(tracker.uuid)
                found = True
        
        if not found:
            video_view = {}
            video_view['mediafile'] = data['mediafile']
            video_view['users'] = []
            video_view['users'].append(tracker.user.id)
            if tracker.time_taken > max_time:
                video_view['time_taken'] = max_time
            else:
                video_view['time_taken'] = tracker.time_taken
            video_view['uuid'] = []
            video_view['uuid'].append(tracker.uuid)
            video_views.append(video_view)
     
    #print video_views   

    out_file = open('/home/alex/temp/hew-video.html', 'w', 'utf-8')
    
    out_file.write("<html>")
    out_file.write("<head>")
    out_file.write('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')
    out_file.write("</head>")
    out_file.write("<body>")
    
    out_file.write("<table>")
    out_file.write("<tr>")
    out_file.write("<th>Media filename</th>")
    out_file.write("<th>No views</th>")
    out_file.write("<th>Total time viewed</th>")
    out_file.write("<th>No users (distinct)</th>")
    out_file.write("</tr>")
             
    for vv in video_views:
        out_file.write("<tr>")
        out_file.write("<td>%s</td>" % vv['mediafile'])
        out_file.write("<td>%d</td>" % len(set(vv['uuid'])))
        out_file.write("<td>%s</td>" % datetime.timedelta(seconds=vv['time_taken']))
        out_file.write("<td>%d</td>" % len(set(vv['users'])))
        out_file.write("</tr>")
        
        print datetime.timedelta(seconds=vv['time_taken'])
        
                    
    out_file.write("</table>")   
    out_file.write("</body></html>")
    out_file.close()

    
def title_lang(title,lang):
    try:
        titles = json.loads(title)
        if lang in titles:
            return titles[lang]
        else:
            for l in titles:
                return titles[l]
    except:
        pass
    return title   
    
if __name__ == "__main__":
    import django
    django.setup()
    run() 