import json
import datetime

def run(): 
    
    from django.contrib.auth.models import User
    from django.db.models import Sum, Max, Min, Avg
    from django.utils.html import strip_tags
    
    from oppia.models import Activity, Course, Cohort, CourseCohort, Participant, Tracker
    from oppia.quiz.models import Quiz, Question, QuizQuestion, QuizAttempt, QuizAttemptResponse
    
    cohort_id = 23
    
    students = User.objects.filter(participant__cohort_id=cohort_id, participant__role=Participant.STUDENT).order_by('username')
    courses = Course.objects.filter(coursecohort__cohort_id = cohort_id, shortname__in=['anc1-et','anc2-et','pnc-et']).order_by('title')
    
    out_file = open('/home/alex/temp/hew-quiz.html', 'w')
    
    out_file.write("<html>")
    out_file.write("<head></head>")
    out_file.write("<body>")
    
    out_file.write("<table>")
    out_file.write("<tr>")
    out_file.write("<th>Course</th>")
    out_file.write("<th>Quiz</th>")
    out_file.write("<th>Question</th>")
    out_file.write("<th>Question Type</th>")
    out_file.write("<th>No attempts</th>")
    out_file.write("<th>No incorrect</th>")
    out_file.write("<th>No partially correct</th>")
    out_file.write("<th>No correct</th>")
    out_file.write("<th>P-score - Difficulty</th>")
    out_file.write("<th>D-Score - Discrimination</th>")
    out_file.write("</tr>")
    
    for c in courses:
        out_file.write("<tr>")
        out_file.write("<td colspan='10'>%s</td>" % title_lang(c.title,"en"))
        print "%s"  % title_lang(c.title,"en")
        print "===================================="
        out_file.write("</tr>")
        quizzes = Activity.objects.filter(section__course=c, type="quiz").exclude(section__order=0).order_by('section__order')
        #quizzes = Activity.objects.filter(section__course=c, type="quiz").order_by('section__order')
        for q in quizzes:
            
            quiz = Quiz.objects.get(quizprops__value=q.digest, quizprops__name="digest")
            out_file.write("<tr><td></td>")
            desc = strip_tags(title_lang(quiz.description,"en").replace(u'\xa0',''))
            out_file.write("<td colspan='9'>%s - %s</td>" % (title_lang(quiz.title,"en"), desc))
            print ("Processing: %s - %s"  % (title_lang(quiz.title,"en"), desc))
            out_file.write("</tr>")
            
            # get questions for quiz
            questions = Question.objects.filter(quizquestion__quiz=quiz).exclude(type='description').order_by("quizquestion__order")
            for qu in questions:
                out_file.write("<tr><td colspan='2'></td>")
                title = strip_tags(title_lang(qu.title,"en").replace(u'\xa0','').replace(u'\u2019','').replace(u'\u2018','').replace(u'\xb0','').replace(u'\xba',''))
                out_file.write("<td width='35%%'>%s</td>" % title)
                out_file.write("<td>%s</td>" % qu.type)
                
                # get no attempts
                qars = QuizAttemptResponse.objects.filter(question=qu,quizattempt__user__in=students)
                
                # get no incorrect/partial/correct
                incorrect = 0
                partial = 0
                correct = 0
                
                for qar in qars:
                    if qar.score == 0:
                        incorrect += 1
                    elif qar.score == 1:
                        correct += 1
                    else:
                        partial += 1
                
                out_file.write("<td>%d</td>" % qars.count())
                out_file.write("<td>%d (%d%%)</td>" % (incorrect, incorrect*100/qars.count()))
                out_file.write("<td>%d (%d%%)</td>" % (partial, partial*100/qars.count()))
                out_file.write("<td>%d (%d%%)</td>" % (correct, correct*100/qars.count()))
                
                
                # calc P & D scores for question
                
                
                if qu.type == 'multichoice':
                    p_score = float(correct) / float(qars.count())
                    out_file.write("<td>%.3f</td>" % (p_score))
                else:
                    out_file.write("<td>-</td>")
                    
                
                top_third = qars.order_by('-score')[:int(qars.count()/3)]
                top_correct_count = 0
                for tt in top_third:
                    if tt.score == 1:
                        top_correct_count += 1
                
                bottom_third = qars.order_by('score')[:int(qars.count()/3)]
                bottom_correct_count = 0
                for bt in bottom_third:
                    if bt.score == 1:
                        bottom_correct_count += 1
                
                d_score = (top_correct_count - bottom_correct_count) * 2.0 / (top_third.count() + bottom_third.count())
                out_file.write("<td>%.3f</td>" % (d_score))
                
                out_file.write("</tr>")
                
        
                    
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