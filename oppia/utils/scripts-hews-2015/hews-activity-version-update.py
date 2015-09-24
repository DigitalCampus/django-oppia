import json
import datetime

def run(): 
    
    from django.contrib.auth.models import User
    from django.db.models import Sum, Max, Min, Avg
    from django.utils.html import strip_tags
    
    from oppia.models import Activity, Course, Cohort, CourseCohort, Participant, Tracker
    from oppia.quiz.models import Quiz, QuizQuestion, QuizAttempt, QuizAttemptResponse
    
    cohort_id = 23

    students = User.objects.filter(participant__cohort_id=cohort_id, participant__role=Participant.STUDENT).order_by('username')
    #courses = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname__in=['anc1-et','anc2-et','pnc-et']).order_by('title')
    courses = Course.objects.filter(coursecohort__cohort_id = cohort_id).order_by('title')
    activities = Activity.objects.filter(section__course__in=courses).values_list('digest',flat=True)
    old_quizzes = []
    old_trackers = []
    for s in students:
        trackers = Tracker.objects.filter(user=s, course__in=courses, type=Activity.QUIZ).exclude(digest__in=activities)
        for t in trackers:
            '''
            print t.activity_title
            print t.section_title
            print t.course.title
            print t.digest
            print t.data
            print "------------------------------------"
            '''
            if t.digest not in old_quizzes:
                old_quizzes.append(t.digest)
                old_trackers.append(t)
    
    #print old_quizzes
    
    quizzes_to_update = [
                        {'old_digest':'0b0897fbf44c51552f8b43a2ce7f42fe17269cr10s2a0p80a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'e05050cd97d83d8f58a5a0a4d7c6409f14218cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'33e3b9b9870c5b1462cb0b83e994773a14227cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'7013f5ebf2e743e7e46fe8547bab616f14243cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'a6447ff50a36a1b0203e362492884a6914254cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'efe989a506a790147457f7f29875341914265cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'2c49008cee999f966b3662c00ee17dfe14276cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'d2cdaade5398e16ddd5699470e49a03a14335cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'99759fc66570c51caa69449b2f83b6d314288cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'5f4a3dfb87daeffccc076993ac269b5c14347cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'10688587b7789e932b4773f5f8204f3d14307cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'b264e9b8f5dc934ee3d3d987a36dc3f614369cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'09131a5ec7897b9877c83cd1cfa84ae914360cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'5c1f41a6ae0fe80ac80b33b017721bd717426cr0s2a1p80a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        {'old_digest':'cb098d67dead4123d33acb418aa1d53214323cr0s1a1p0a0',
                         'new_digest': '',
                         'old_quiz_id':0,
                         'new_quiz_id':0,},
                        ]
    for t in old_trackers:
        #get quiz id
        for qtu in quizzes_to_update:
            if qtu['old_digest'] == t.digest:
                print t.data
                new_act = Activity.objects.get(section__course=t.course, section__title=t.section_title, title =t.activity_title)
                print new_act
                qtu['new_digest'] = new_act.digest
                quiz = Quiz.objects.get(quizprops__value=new_act.digest)
                qtu['new_quiz_id'] = quiz.id
                data_obj = json.loads(t.data)
                qtu['old_quiz_id'] = int(data_obj['quiz_id'])
                
    print quizzes_to_update           
        
        
    
    for qtu in quizzes_to_update:
        
        #Update all Tracker objects
        trackers = Tracker.objects.filter(digest=qtu['old_digest'])
        print trackers.count()
        for t in trackers:
            t.digest = qtu['new_digest']
            data_obj = json.loads(t.data)
            data_obj['quiz_id'] = qtu['new_quiz_id'] 
            t.data = json.dumps(data_obj)
            t.save()
          
        #Update all quiz attempts
        quiz_attempts = QuizAttempt.objects.filter(quiz__id=qtu['old_quiz_id'])
        new_quiz = Quiz.objects.get(pk=qtu['new_quiz_id'])
        print quiz_attempts.count()
        for qa in quiz_attempts:
            qa.quiz = new_quiz
            qa.save()
    '''
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
    
    out_file.write("</table>")   
    out_file.write("</body></html>")
    out_file.close()
    '''
        
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