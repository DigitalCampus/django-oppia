
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.models import Activity
from quiz.models import Quiz, \
                        QuizAttempt, \
                        Question
from settings.models import SettingProperties
from settings import constants


class Command(BaseCommand):
    help = _(u"Cleans up unused/old quizzes and questions")

    def handle(self, *args, **options):
        # remove duplicates
        self.check_duplicates()

        # remove quizzes with no quizprops digest
        self.check_no_digest()

        # remove quizzes with no responses for X years
        self.check_old_quizzes()

        # remove questions not attached to quizzes
        self.delete_questions_with_no_quiz()

    def check_duplicates(self):
        act_quizzes = Activity.objects.filter(type=Activity.QUIZ)
        for aq in act_quizzes:
            quizzes = Quiz.objects.filter(quizprops__value=aq.digest,
                                          quizprops__name="digest")
            if quizzes.count() > 1:
                self.delete_duplicate(aq.digest, quizzes)

    def delete_duplicate(self, digest, quizzes):
        print(_(u"Quiz {} has {} associated quiz objects:")
              .format(digest, quizzes.count()))
        for quiz in quizzes:
            attempts = QuizAttempt.objects \
                .filter(quiz=quiz).count()
            print(_(u"\tQuiz {} has {} attempts").format(quiz,
                                                         attempts))

            if attempts == 0:
                print(_(u"Deleting quiz {}, as it has no attempts and is a \
                    duplicate").format(quiz.title))
                self.delete_quiz(quiz)

    def check_no_digest(self):
        quizzes = Quiz.objects.filter(quizprops__isnull=True)
        for quiz in quizzes:
            print(_(u"Deleting quiz {}, as it has no digest")
                  .format(quiz.title))
            quiz.delete()

    def check_old_quizzes(self):
        years = SettingProperties.get_property(
            constants.OPPIA_DATA_RETENTION_YEARS, 999)
        archive_date = timezone.now() - relativedelta(years=years)
        quizzes = Quiz.objects.filter(created_date__lte=archive_date)
        for quiz in quizzes:
            qas = QuizAttempt.objects.filter(quiz=quiz, user__is_staff=False)
            if qas.count() == 0:
                print(_(u"Deleting quiz {}, as it was created over {} years \
                    ago and has no attempts").format(quiz.title, years))
                self.delete_quiz(quiz)

    def delete_quiz(self, quiz):
        quiz.delete()
        print(_(u"quiz deleted"))

    def delete_questions_with_no_quiz(self):
        questions = Question.objects.filter(quizquestion__isnull=True)
        for question in questions:
            print(_(u"Deleting question {}, as it is not attached to any \
                quiz").format(question.title))
            question.delete()
