
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

        quiz_act_digests = Activity.objects.filter(type=Activity.QUIZ).values_list('digest', flat=True)
        quiz_old_digests = QuizProps.objects.filter(name="digest") \
            .exclude(value__in=quiz_act_digests) \
            .values_list('value', flat=True)

        quizzes = Quiz.objects.filter(quizprops__value__in=quiz_old_digests, quizprops__name="digest")
        quizzes_attempts = QuizAttempt.objects.all().values('quiz').distinct()

        to_delete = {}
        to_delete['Quizzes'] = quizzes.exclude(pk__in=quizzes_attempts)  # quizzes without attempts
        to_delete['QuizProps'] = QuizProps.objects.filter(quiz__in=list(to_delete['Quizzes'].values_list(flat=True)))
        to_delete['QuizQuestions'] = QuizQuestion.objects.filter(quiz__in=to_delete['Quizzes'])
        to_delete['Questions'] = Question.objects.filter(quizquestion__quiz__in=to_delete['Quizzes'])
        to_delete['QuestionProps'] = QuestionProps.objects.filter(question__in=to_delete['Questions'])
        to_delete['Responses'] = Response.objects.filter(question__in=to_delete['Questions'])
        to_delete['ResponseProps'] = ResponseProps.objects.filter(response__in=to_delete['Responses'])

        self.stdout.write(self.style.MIGRATE_HEADING("Summary of deletions:"))
        total = 0
        for key in to_delete:
            elem_count = to_delete[key].count()
            total += elem_count
            self.stdout.write(
                self.style.MIGRATE_LABEL("  * " + key + ":") + ' %d items to delete' % elem_count)

        if total is 0:
            self.stdout.write(self.style.MIGRATE_SUCCESS("No new elements to clean up."))
        else:
            if self.prompt("You are about to delete %d records, are you sure?" % total):
                self.stdout.write("Deleting... (may take a while)")
                # we have to delete them in order, so we cannot traverse de dict
                to_delete['ResponseProps'].delete()
                to_delete['Responses'].delete()
                to_delete['QuizQuestions'].delete()
                to_delete['QuestionProps'].delete()
                to_delete['Questions'].delete()
                to_delete['QuizProps'].delete()
                to_delete['Quizzes'].delete()
                self.stdout.write(self.style.MIGRATE_SUCCESS("Quizzes cleaned up :)"))
