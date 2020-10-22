

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from oppia.management import commands
from oppia.models import Course
from quiz.models import Quiz, Question, QuizAttemptResponse


class Command(BaseCommand):
    help = 'Generates the discrimination index for each question in the given quiz'
    
    def add_arguments(self, parser):

        # Required quiz digest argument
        parser.add_argument(
            'digest',
            help='quiz digest',
            type=str,
            nargs='?',
        )
    
    def handle(self, *args, **options):
        digest = options['digest']
        
        # get the quiz
        try:
            quiz = Quiz.objects.get(quizprops__name='digest', quizprops__value=digest)
        except Quiz.DoesNotExist:
            print(commands.TERMINAL_COLOUR_WARNING)
            print(_(u"Quiz digest not found"))
            print(commands.TERMINAL_COLOUR_ENDC)
            return
        
        course = Course.objects.get(section__activity__digest=digest)
        print(course)
        print(quiz)
        
        # get the questions (in order)
        questions = Question.objects.filter(quizquestion__quiz=quiz)
       
        # loop to generate difficulty index for each question
        for question in questions:
            print(question.get_title("en"))
            qars = QuizAttemptResponse.objects.filter(question=question, quizattempt__user__is_staff=False).order_by('-score')
            total_count = qars.count()
            
            top_slice_start = 0
            top_slice_end = int(total_count/(10/3))
            bottom_slice_start = total_count - top_slice_end
            bottom_slice_end = total_count -1
            
            top_slice = qars.values_list('id', flat=True)[top_slice_start:top_slice_end]
            top_slice_ids = [ts for ts in top_slice]
            #print(top_slice[top_slice_start:top_slice_end])
            top_slice_correct = QuizAttemptResponse.objects.filter(score__gt=0, pk__in=top_slice_ids).count()
                
            bottom_slice = qars.values_list('id', flat=True)[bottom_slice_start:bottom_slice_end]
            bottom_slice_ids = [ts for ts in bottom_slice]
            bottom_slice_correct = QuizAttemptResponse.objects.filter(score__gt=0, pk__in=bottom_slice_ids).count()
            
            disc_index = ((top_slice_correct - bottom_slice_correct)/(top_slice.count() + bottom_slice.count())) * 2 * 100
            print(_(u"Discrimination Index: %0.0f") % disc_index)
            if disc_index < 40:
                print(commands.TERMINAL_COLOUR_WARNING)
                print(_(u"This question might not be useful to distinguish between high and low performing users"))
                print(commands.TERMINAL_COLOUR_ENDC)
                
            print("\n")
            
            
                