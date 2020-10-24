

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from oppia.management import commands
from oppia.models import Course
from quiz.models import Quiz, Question, QuizAttemptResponse

from quiz import constants

class Command(BaseCommand):
    help = 'Generates the difficulty and dicrimintation index for each \
        question in the given quiz'
    
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
            quiz = Quiz.objects.get(quizprops__name='digest',
                                    quizprops__value=digest)
            print(quiz)
        except Quiz.DoesNotExist:
            print(commands.TERMINAL_COLOUR_WARNING)
            print(_(u"Quiz digest not found"))
            print(commands.TERMINAL_COLOUR_ENDC)
            return
        
        try:
            course = Course.objects.get(section__activity__digest=digest)
            print(course)
        except Course.DoesNotExist:
            print(_(u"Course not found, perhaps this is now an unused quiz?"))

        # get the questions (in order)
        questions = Question.objects.filter(quizquestion__quiz=quiz)
       
        # loop to generate difficulty index for each question
        for question in questions:
            print("[%d] %s" % (question.id, question.get_title("en")))
            print("No responses: %d" % question.get_no_responses())
            if question.get_no_responses() > constants.MIN_NO_RESPONSES_FOR_INDICES:
                difficulty_index = question.get_difficulty_index()
                print(_(u"Difficulty Index: %0.2f") % difficulty_index)
                if difficulty_index > 0.90:
                    print(commands.TERMINAL_COLOUR_WARNING)
                    print(_(u"This question might be too easy for users"))
                    print(commands.TERMINAL_COLOUR_ENDC)
                    
                if difficulty_index < 0.30:
                    print(commands.TERMINAL_COLOUR_WARNING)
                    print(_(u"This question might be too difficult for users"))
                    print(commands.TERMINAL_COLOUR_ENDC)
                    
                disc_index = question.get_discrimination_index()
                print(_(u"Discrimination Index: %0.0f %%") 
                      % disc_index)
                if disc_index < 40:
                    print(commands.TERMINAL_COLOUR_WARNING)
                    print(_(u"This question might not be useful to distinguish between high and low performing users"))
                    print(commands.TERMINAL_COLOUR_ENDC)
            else:
                print(commands.TERMINAL_COLOUR_WARNING)
                print(_(u"There are not enough responses yet for this index to be useful"))
                print(commands.TERMINAL_COLOUR_ENDC)
                
            print("\n")
        