import json

def run(): 
    
    from django.contrib.auth.models import User
    from django.db.models import Sum, Max, Min, Avg
    from django.utils.html import strip_tags
    
    from oppia.models import Activity, Course, Cohort, CourseCohort, Participant
    from oppia.quiz.models import Quiz, QuizQuestion, QuizAttempt, QuizAttemptResponse
    
    PASS_THRESHOLD = 50 
    cohort_id = 23
    
    students = User.objects.filter(participant__cohort_id=cohort_id, participant__role=Participant.STUDENT).order_by('username')
    courses = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname__in=['anc1-et','anc2-et','pnc-et']).order_by('title')
    
    out_file = open('/home/alex/temp/hew-detail-%d-percent.html' % (PASS_THRESHOLD), 'w')
    
    out_file.write("<html>")
    out_file.write("<head></head>")
    out_file.write("<body>")
    
    out_file.write("<table>")
    out_file.write("<tr>")
    out_file.write("<th>Student</th>")
    out_file.write("<th>Course/Quiz</th>")
    out_file.write("<th>No Attempts</th>")
    out_file.write("<th>Max Score (%)</th>")
    out_file.write("<th>Min Score (%)</th>")
    out_file.write("<th>Avg Score (%)</th>")
    out_file.write("<th>First Score (%)</th>")
    out_file.write("<th>Recent Score (%)</th>")
    out_file.write("</tr>")
    
    for s in students:
        print s.first_name + " " + s.last_name
        out_file.write("<tr>")
        out_file.write("<td colspan='8'>%s %s</td>" % (s.first_name, s.last_name))
        out_file.write("</tr>")
        
        for c in courses:
            print c.shortname
            out_file.write("<tr>")
            out_file.write("<td></td><td colspan='7'><b>%s</b></td>" % c.shortname.upper())
            out_file.write("</tr>")
            
            course_summary_baseline = None
            
            # get baseline quiz for this course
            # baseline - no times taken, max score, min score, first score, most recent score, average score
            baseline = Activity.objects.filter(section__course=c, baseline=True, type="quiz")
            for b in baseline:
               
                quiz = Quiz.objects.get(quizprops__value=b.digest, quizprops__name="digest")
                attempts = QuizAttempt.objects.filter(quiz=quiz, user=s)
                no_attempts = attempts.count()
                
                print "Baseline:"
                out_file.write("<tr>")
                out_file.write("<td></td><td>%s</td>" % (title_lang(quiz.title,"en")))
                
                print "No attempts: " + str(no_attempts)
                out_file.write("<td>" + str(no_attempts) + "</td>")
                if attempts.count() != 0:
                    max_score = 100*float(attempts.aggregate(max=Max('score'))['max']) / float(attempts[0].maxscore)
                    course_summary_baseline = max_score
                    
                    min_score = 100*float(attempts.aggregate(min=Min('score'))['min']) / float(attempts[0].maxscore)
                    avg_score = 100*float(attempts.aggregate(avg=Avg('score'))['avg']) / float(attempts[0].maxscore)
                    first_date = attempts.aggregate(date=Min('attempt_date'))['date']
                    recent_date = attempts.aggregate(date=Max('attempt_date'))['date']
                    first_score = 100*float(attempts.filter(attempt_date = first_date)[0].score) / float(attempts[0].maxscore)
                    latest_score = 100*float(attempts.filter(attempt_date = recent_date)[0].score) / float(attempts[0].maxscore)
                    
                    print "Max Score: " + str(max_score)
                    out_file.write("<td>%0.1f</td>" % max_score)
                    
                    print "Min Score: " + str(min_score)
                    out_file.write("<td>%0.1f</td>" % min_score)
                    
                    print "Avg Score: " + str(avg_score)
                    out_file.write("<td>%0.1f</td>" % avg_score)
                    
                    print "First Score: " + str(first_score)
                    out_file.write("<td>%0.1f</td>" % first_score)
                    
                    print "Latest Score: "+ str(latest_score)
                    out_file.write("<td>%0.1f</td>" % latest_score)
                else:
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
            
                out_file.write("</tr>\n")
            
            # other quizzes - no times taken, max score, min score, first score, most recent score, average score
            quizzes = Activity.objects.filter(section__course=c, baseline=False, type="quiz").order_by('section__order')
            
            course_summary_total_no_questions = 0
            course_summary_no_questions_correct = 0
            course_summary_attempted_all = True
            course_summary_passed_all = True
            for q in quizzes:
                
                quiz = Quiz.objects.get(quizprops__value=q.digest, quizprops__name="digest")
                attempts = QuizAttempt.objects.filter(quiz=quiz, user=s)
                no_attempts = attempts.count()
                
                course_summary_total_no_questions += QuizQuestion.objects.filter(quiz=quiz).count()
                
                print "Quizzes:"
                print title_lang(quiz.title,"en")
                
                out_file.write("<tr>")
                title = title_lang(quiz.title,"en")
                desc = strip_tags(title_lang(quiz.description,"en").replace(u'\xa0',''))
                out_file.write("<td></td><td>%s (%s)</td>" % (title,desc))
                
                print "No attempts: " + str(no_attempts)
                out_file.write("<td>%d</td>" % no_attempts)
                
                if attempts.count() != 0:
                    max_score = 100*float(attempts.aggregate(max=Max('score'))['max']) / float(attempts[0].maxscore)
                    course_summary_no_questions_correct += attempts.aggregate(max=Max('score'))['max']
                    
                    min_score = 100*float(attempts.aggregate(min=Min('score'))['min']) / float(attempts[0].maxscore)
                    avg_score = 100*float(attempts.aggregate(avg=Avg('score'))['avg']) / float(attempts[0].maxscore)
                    first_date = attempts.aggregate(date=Min('attempt_date'))['date']
                    recent_date = attempts.aggregate(date=Max('attempt_date'))['date']
                    first_score = 100*float(attempts.filter(attempt_date = first_date)[0].score) / float(attempts[0].maxscore)
                    latest_score = 100*float(attempts.filter(attempt_date = recent_date)[0].score) / float(attempts[0].maxscore)
                   
                    print "Max Score: " + str(max_score)
                    out_file.write("<td>%0.1f</td>" % max_score)
                    
                    print "Min Score: " + str(min_score)
                    out_file.write("<td>%0.1f</td>" % min_score)
                    
                    print "Avg Score: " + str(avg_score)
                    out_file.write("<td>%0.1f</td>" % avg_score)
                    
                    print "First Score: " + str(first_score)
                    out_file.write("<td>%0.1f</td>" % (first_score))
                    
                    print "Latest Score: "+ str(latest_score)
                    out_file.write("<td>%0.1f</td>" % (latest_score))
                    
                    if max_score < 80:
                        course_summary_passed_all = False
                else:
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
                    out_file.write("<td>-</td>")
                    course_summary_attempted_all = False
                    course_summary_passed_all = False
            
                out_file.write("</tr>\n")
            # over all for course
            out_file.write("<tr>")
            out_file.write("<td></td><td>Total score for course:</td>")
            course_total_score = course_summary_no_questions_correct * 100/course_summary_total_no_questions
            out_file.write("<td colspan='6'>%0.1f</td>" % course_total_score)
            out_file.write("</tr>\n")
            
            out_file.write("<tr>")
            out_file.write("<td></td><td>Attempted all quizzes</td>")
            if course_summary_attempted_all:
                out_file.write("<td colspan='6'>True</td>")
            else:
                out_file.write("<td colspan='6'>False</td>")
            out_file.write("</tr>\n")
            
            out_file.write("<tr>")
            out_file.write("<td></td><td>Passed all quizzes</td>")
            if course_summary_passed_all:
                out_file.write("<td colspan='6'>True</td>")
            else:
                out_file.write("<td colspan='6'>False</td>")
            out_file.write("</tr>\n")
            
            out_file.write("<tr>")
            out_file.write("<td></td><td>Improvement on baseline</td>")
            if course_summary_baseline and course_summary_attempted_all:
                improvement = float(course_total_score) - float(course_summary_baseline)
                out_file.write("<td colspan='6'>%0.1f</td>" % (improvement))
            else:
                out_file.write("<td colspan='6'>-</td>")
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