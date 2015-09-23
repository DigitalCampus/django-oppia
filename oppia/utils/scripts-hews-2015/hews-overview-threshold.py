import json

def run(): 
    
    from django.contrib.auth.models import User
    from django.db.models import Sum, Max, Min, Avg
    from django.utils.html import strip_tags
    
    from oppia.models import Activity, Course, Cohort, CourseCohort, Participant, Tracker
    from oppia.quiz.models import Quiz, QuizQuestion, QuizAttempt, QuizAttemptResponse
    
    PASS_THRESHOLD = 50 
    cohort_id = 23
    
    students = User.objects.filter(participant__cohort_id=cohort_id, participant__role=Participant.STUDENT).order_by('username')
    courses = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname__in=['anc1-et','anc2-et','pnc-et']).order_by('title')
    
    out_file = open('/home/alex/temp/hew-overview-%d-percent.html' % (PASS_THRESHOLD), 'w')
    
    out_file.write("<html>")
    out_file.write("<head></head>")
    out_file.write("<body>")
    
    out_file.write("<h3>Quiz pass threshold set at: %d%%</h3>" % PASS_THRESHOLD)
    out_file.write("<table>")
    out_file.write("<tr>")
    out_file.write("<th>Student</th>")
    out_file.write("<th>No Quizzes</th>")
    out_file.write("<th>No Attempted</th>")
    out_file.write("<th>No Passed</th>")
    out_file.write("</tr>")
    
    for s in students:
        print s.first_name + " " + s.last_name
        out_file.write("<tr>")
        out_file.write("<td>%s %s</td>" % (s.first_name, s.last_name))
        
        
        no_quizzes = 0
        no_attempted = 0
        no_passed = 0
        
        for c in courses:       
            # other quizzes - no times taken, max score, min score, first score, most recent score, average score
            act_quizzes = Activity.objects.filter(section__course=c, baseline=False, type="quiz")
            no_quizzes += act_quizzes.count()
              
            quiz_digests = act_quizzes.values_list('digest', flat=True).distinct()
            
            quizzes = Quiz.objects.filter(quizprops__name='digest', quizprops__value__in=quiz_digests)
            
            for q in quizzes:
                qas = QuizAttempt.objects.filter(quiz=q,user=s).aggregate(user_max_score=Max('score'), max_score=Max('maxscore'))
                print qas
                
                if qas['user_max_score'] is not None:
                    no_attempted += 1
                    
                    if qas['user_max_score'] * 100/ qas['max_score'] >= PASS_THRESHOLD:
                        no_passed += 1

        out_file.write("<td>%d</td>" % no_quizzes) 
        out_file.write("<td>%d</td>" % no_attempted) 
        out_file.write("<td>%d</td>" % no_passed)   
        out_file.write("</tr>\n")        
            
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