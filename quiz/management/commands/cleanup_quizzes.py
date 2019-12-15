
from distutils.util import strtobool

from django.core.management.base import BaseCommand

from oppia.models import Activity
from quiz.models import Quiz, \
                        QuizProps, \
                        QuizAttempt, \
                        Response, \
                        ResponseProps, \
                        Question, \
                        QuestionProps, \
                        QuizQuestion


class Command(BaseCommand):
    help = 'Cleans up old data (quizzes and questions) that are not relevant \
            anymore'

    def prompt(self, query):
        self.stdout.write('%s [y/n]: ' % query)
        val = input()
        try:
            ret = strtobool(val)
        except ValueError:
            self.stdout.write('Please answer with a y/n\n')
            return self.prompt(query)
        return ret

    def print_waiting_dot(self):
        self.stdout.write("..", ending='')
        self.stdout.flush()

    def remove_duplicate_quizzes(self):
        act_quizzes = Activity.objects.filter(type=Activity.QUIZ)
        for aq in act_quizzes:
            try:
                quizobjs = Quiz.objects.filter(quizprops__value=aq.digest,
                                               quizprops__name="digest")
                quiz_to_delete = []
                if quizobjs.count() > 1:
                    self.stdout \
                        .write("\nQuiz {} has {} associated quiz objects:\n"
                               .format(aq.digest, quizobjs.count()))
                    for quiz in quizobjs:
                        attempts = QuizAttempt.objects \
                            .filter(quiz=quiz).count()
                        if not attempts:
                            quiz_to_delete.append(quiz)
                        self.stdout.write(
                            "    Quiz {} has {} attempts\n".format(quiz,
                                                                   attempts))

                    if len(quiz_to_delete) > 0:
                        self.stdout.write(
                            "    > Do you want to remove the {} quizzes \
                             without attempts?\n".format(len(quiz_to_delete)))

            except Quiz.DoesNotExist:
                pass
            
    def handle(self, *args, **options):

        self.remove_duplicate_quizzes()

        quiz_act_digests = Activity.objects \
            .filter(type=Activity.QUIZ) \
            .values_list('digest', flat=True)
        quiz_old_digests = QuizProps.objects.filter(name="digest") \
            .exclude(value__in=quiz_act_digests) \
            .values_list('value', flat=True)

        quizzes = Quiz.objects.filter(quizprops__value__in=quiz_old_digests,
                                      quizprops__name="digest")
        quizzes_attempts = QuizAttempt.objects.all().values('quiz').distinct()

        to_delete = {}
        # quizzes without attempts
        to_delete['Quizzes'] = quizzes.exclude(pk__in=quizzes_attempts)
        to_delete['QuizProps'] = QuizProps.objects \
            .filter(quiz__in=list(to_delete['Quizzes']
                                  .values_list(flat=True)))
        to_delete['QuizQuestions'] = QuizQuestion.objects \
            .filter(quiz__in=to_delete['Quizzes'])
        to_delete['Questions'] = Question.objects \
            .filter(quizquestion__quiz__in=to_delete['Quizzes'])
        to_delete['QuestionProps'] = QuestionProps.objects \
            .filter(question__in=to_delete['Questions'])
        to_delete['Responses'] = Response.objects \
            .filter(question__in=to_delete['Questions'])
        to_delete['ResponseProps'] = ResponseProps.objects \
            .filter(response__in=to_delete['Responses'])

        self.stdout.write(self.style.MIGRATE_HEADING("Summary of deletions:"))
        total = 0
        for key in to_delete:
            elem_count = to_delete[key].count()
            total += elem_count
            self.stdout.write(
                self.style.MIGRATE_LABEL("  * " + key + ":")
                + ' %d items to delete' % elem_count)

        if total == 0:
            self.stdout.write("No new elements to clean up.")
        else:
            if self.prompt("You are about to delete %d records, are you sure?"
                           % total):
                self.stdout.write("Deleting... (may take a while)")
                # we have to delete them in order, so we cannot traverse the
                # dict
                to_delete['ResponseProps'].delete()
                to_delete['Responses'].delete()
                to_delete['QuizQuestions'].delete()
                to_delete['QuestionProps'].delete()
                to_delete['Questions'].delete()
                to_delete['QuizProps'].delete()
                to_delete['Quizzes'].delete()
                self.stdout.write("Quizzes cleaned up :)")
