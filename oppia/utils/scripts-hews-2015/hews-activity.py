import json
import datetime

def run(): 
    
    from django.contrib.auth.models import User
    from django.db.models import Sum, Max, Min, Avg
    from django.utils.html import strip_tags
    
    from oppia.models import Activity, Course, Cohort, CourseCohort, Participant, Tracker
    from oppia.quiz.models import Quiz, QuizQuestion, QuizAttempt, QuizAttemptResponse
    
    cohort_id = 23
    course_start_date = datetime.datetime(2015,05,1,0,0,0)
    course_weeks = 8
    
    students = User.objects.filter(participant__cohort_id=cohort_id, participant__role=Participant.STUDENT).order_by('username')
    courses = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname__in=['anc1-et','anc2-et','pnc-et']).order_by('title')
    
    out_file = open('/home/alex/temp/hew-activity.html', 'w')
    
    out_file.write("<html>")
    out_file.write("<head></head>")
    out_file.write("<body>")
    
    out_file.write("<table>")
    out_file.write("<tr>")
    out_file.write("<th>Student</th>")
    out_file.write("<th>No Weeks</th>")
    out_file.write("<th>Weeks with activity</th>")
    out_file.write("<th>Every Week?</th>")
    out_file.write("</tr>")
    
    for s in students:
        print s.first_name + " " + s.last_name
        out_file.write("<tr>")
        out_file.write("<td>%s %s</td>" % (s.first_name, s.last_name))
        
        weeks_activity = 0
        
        for i in range(0,course_weeks):
            start_date = course_start_date + datetime.timedelta(days=(i*7))
            end_date = course_start_date + datetime.timedelta(days=((i+1)*7))
            activity = Tracker.objects.filter(user_id=s.id,tracker_date__gte=start_date,tracker_date__lt=end_date).count()
            if activity > 0:
                weeks_activity += 1
            
        
    
        if weeks_activity == course_weeks:
            every_week = True
        else:
            every_week = False
            
        out_file.write("<td>%d</td>" % course_weeks) 
        out_file.write("<td>%d</td>" % weeks_activity) 
        out_file.write("<td>%d</td>" % every_week)   
        out_file.write("</tr>\n")
        
        # overall for all courses
        
            
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