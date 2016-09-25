from django.core.management.base import BaseCommand, CommandError

from oppia.models import Activity
from oppia.quiz.models import Quiz, QuizProps, QuizAttempt


class Command(BaseCommand):
    help = 'Cleans up old data that is not relevant anymore'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        quiz_activities = Activity.objects.filter(type=Activity.QUIZ).values_list('digest', flat=True)
        quiz_old_digests = QuizProps.objects.filter(name="digest")\
                            .exclude(value__in=quiz_activities)\
                            .values_list('value', flat=True)

        quizzes = Quiz.objects.filter(quizprops__value__in=quiz_old_digests, quizprops__name="digest")
        quizzes_attempts = QuizAttempt.objects.all().values('quiz').distinct()
        quizzes_without_attempts = quizzes.exclude(pk__in=quizzes_attempts)

        print Quiz.objects.all().count()
        print quiz_activities.count()
        print quiz_old_digests.count()
        print quizzes.count()
        print quizzes_attempts.count()
        print quizzes_without_attempts.count()

        raise CommandError('Poll does not exist')
