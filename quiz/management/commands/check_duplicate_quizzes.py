
import oppia.management.commands

from distutils.util import strtobool

from django.core.management.base import BaseCommand

from oppia.models import Activity
from quiz.models import Quiz, QuizProps, QuizAttempt, Response, ResponseProps, Question, QuestionProps, \
    QuizQuestion

class Command(BaseCommand):
    help = 'Cleans up old data (quizzes and questions) that is not relevant anymore'

    def add_arguments(self, parser):
        pass

    def prompt(self, query):
        self.stdout.write('%s [y/n]: ' % query)
        val = raw_input()
        try:
            ret = strtobool(val)
        except ValueError:
            self.stdout.write('Please answer with a y/n\n')
            return self.prompt(query)
        return ret

    def print_waiting_dot(self):
        self.stdout.write("..", ending='')
        self.stdout.flush()

    def handle(self, *args, **options):

        act_quizzes = Activity.objects.filter(type=Activity.QUIZ)
        for aq in act_quizzes:
            try:
                quizobjs = Quiz.objects.filter(quizprops__value=aq.digest, quizprops__name="digest")
                quiz_to_delete = []
                if quizobjs.count() > 1:
                    self.stdout.write("\nQuiz {} has {} associated quiz objects:\n".format(aq.digest, quizobjs.count()))
                    for quiz in quizobjs:
                        attempts = QuizAttempt.objects.filter(quiz=quiz).count()
                        if not attempts:
                            quiz_to_delete.append(quiz)
                        self.stdout.write(
                            "    Quiz {} has {} attempts\n".format(quiz, attempts))

                    if len(quiz_to_delete) > 0:
                        self.stdout.write(
                            "    > Do you want to remove the {} quizzes without attempts?\n".format(len(quiz_to_delete)))

            except Quiz.DoesNotExist:
                pass

