'''
 Script to remove unused quiz questions
 
 For full instructions, see the documentation at 
 https://oppiamobile.readthedocs.org/en/latest/
'''

from oppia.models import Activity
from oppia.quiz.models import Quiz, QuizProps, QuizQuestion, Question


def run():
    
    # find all the current quizzes via md5 in current activities
    quiz_acts = Activity.objects.filter(type='quiz').values('digest').distinct()
    print quiz_acts.count()
    
    
    quiz_props = QuizProps.objects.filter(name='digest').exclude(value__in=Activity.objects.filter(type='quiz').values_list('digest',flat=True))
    print quiz_props.count()
    
    quiz_question = Question.objects.filter()
    print quiz_question.count()
    
    #for q in quiz_question:
    #    print q.question.title

                
if __name__ == "__main__":
    run() 