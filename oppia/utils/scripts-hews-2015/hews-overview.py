import json

def run(): 
    
    from django.contrib.auth.models import User
    from django.db.models import Sum, Max, Min, Avg
    from django.utils.html import strip_tags
    
    from oppia.models import Activity, Course, Cohort, CourseCohort, Participant, Tracker
    from oppia.quiz.models import Quiz, QuizQuestion, QuizAttempt, QuizAttemptResponse
    
    cohort_id = 23
    
    students = User.objects.filter(participant__cohort_id=cohort_id, participant__role=Participant.STUDENT).order_by('username')
    anc1 = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname='anc1-et').order_by('title')
    anc2 = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname='anc2-et').order_by('title')
    pnc = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname='pnc-et').order_by('title')
    #all_courses = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname__in=['anc1-et','anc2-et','pnc-et']).order_by('title')
    
    out_file = open('/home/alex/temp/hew-overview.html', 'w')
    
    out_file.write("<html>")
    out_file.write("<head><style> td {text-align:center;}</style></head>")
    out_file.write("<body>")
    
    out_file.write("<table>")
    out_file.write("<tr>")
    out_file.write("<th>&nbsp;</th>")
    
    out_file.write("<th colspan=3>ANC 1</th>")
    out_file.write("<th colspan=3>ANC 2</th>")
    out_file.write("<th colspan=3>PNC</th>")
    
    out_file.write("<th colspan=3>Total</th>")
    out_file.write("</tr>")
    out_file.write("<tr>")
    out_file.write("<th>Student</th>")
    
    out_file.write("<th>No Quizzes</th>")
    out_file.write("<th>No Attempted</th>")
    out_file.write("<th>No Passed</th>")
    out_file.write("<th>No Quizzes</th>")
    out_file.write("<th>No Attempted</th>")
    out_file.write("<th>No Passed</th>")
    out_file.write("<th>No Quizzes</th>")
    out_file.write("<th>No Attempted</th>")
    out_file.write("<th>No Passed</th>")
    
    out_file.write("<th>No Quizzes</th>")
    out_file.write("<th>No Attempted</th>")
    out_file.write("<th>No Passed</th>")
    out_file.write("</tr>")
    
    for s in students:
        print s.first_name + " " + s.last_name
        out_file.write("<tr>")
        out_file.write("<td>%s %s</td>" % (s.first_name, s.last_name))
        
        anc1_no_quizzes = 0
        anc1_no_attempted = 0
        anc1_no_passed = 0
        
        for c in anc1:       
            # other quizzes - no times taken, max score, min score, first score, most recent score, average score
            quizzes = Activity.objects.filter(section__course=c, baseline=False, type="quiz")
            anc1_no_quizzes += quizzes.count()
              
            quiz_digests = quizzes.values_list('digest', flat=True).distinct()
            
            attempted = Tracker.objects.filter(user_id=s.id, digest__in=quiz_digests).values_list('digest', flat=True).distinct()
            anc1_no_attempted += attempted.count()
                
            passed = Tracker.objects.filter(user_id=s.id, digest__in=quiz_digests, completed=True).values_list('digest', flat=True).distinct()
            anc1_no_passed += passed.count()
        
        
        out_file.write("<td>%d</td>" % anc1_no_quizzes) 
        out_file.write("<td>%d</td>" % anc1_no_attempted) 
        out_file.write("<td>%d</td>" % anc1_no_passed) 
        
            
        anc2_no_quizzes = 0  
        anc2_no_attempted = 0
        anc2_no_passed = 0
        
        for c in anc2:       
            # other quizzes - no times taken, max score, min score, first score, most recent score, average score
            quizzes = Activity.objects.filter(section__course=c, baseline=False, type="quiz")
            anc2_no_quizzes += quizzes.count()
              
            quiz_digests = quizzes.values_list('digest', flat=True).distinct()
            
            attempted = Tracker.objects.filter(user_id=s.id, digest__in=quiz_digests).values_list('digest', flat=True).distinct()
            anc2_no_attempted += attempted.count()
                
            passed = Tracker.objects.filter(user_id=s.id, digest__in=quiz_digests, completed=True).values_list('digest', flat=True).distinct()
            anc2_no_passed += passed.count()
        
        
        out_file.write("<td>%d</td>" % anc2_no_quizzes) 
        out_file.write("<td>%d</td>" % anc2_no_attempted) 
        out_file.write("<td>%d</td>" % anc2_no_passed) 
        
            
        pnc_no_quizzes = 0
        pnc_no_attempted = 0
        pnc_no_passed = 0
        
        for c in pnc:       
            # other quizzes - no times taken, max score, min score, first score, most recent score, average score
            quizzes = Activity.objects.filter(section__course=c, baseline=False, type="quiz")
            pnc_no_quizzes += quizzes.count()
              
            quiz_digests = quizzes.values_list('digest', flat=True).distinct()
            
            attempted = Tracker.objects.filter(user_id=s.id, digest__in=quiz_digests).values_list('digest', flat=True).distinct()
            pnc_no_attempted += attempted.count()
                
            passed = Tracker.objects.filter(user_id=s.id, digest__in=quiz_digests, completed=True).values_list('digest', flat=True).distinct()
            pnc_no_passed += passed.count()
        
       
        out_file.write("<td>%d</td>" % pnc_no_quizzes) 
        out_file.write("<td>%d</td>" % pnc_no_attempted) 
        out_file.write("<td>%d</td>" % pnc_no_passed) 
        
        
        no_quizzes = pnc_no_quizzes + anc1_no_quizzes + anc2_no_quizzes
        no_attempted = pnc_no_attempted + anc1_no_attempted + anc2_no_attempted
        no_passed = pnc_no_passed + anc1_no_passed + anc2_no_passed
        
        out_file.write("<td>%d</td>" % no_quizzes) 
        out_file.write("<td>%d</td>" % no_attempted) 
        out_file.write("<td>%d</td>" % no_passed)   
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