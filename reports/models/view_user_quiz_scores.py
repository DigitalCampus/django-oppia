from django.db import models
from django.db.models import F, Q

from dbview.models import DbView

from profile.models import UserProfileCustomField
from quiz.models import Quiz, QuizAttempt, QuizProps


class ViewUserQuizScores(DbView):

    @classmethod
    def view(cls):
        #.filter(Q(quiz__quizprops__name="courseversion") 
            #| Q(quizprops__name="moodle_quiz_id") ) \
        qs = QuizAttempt.objects.filter(
            user__is_staff=False,
            user__is_superuser=False,
            user__userprofile__exclude_from_reporting=False,
            event='\"quiz_attempt\"') \
            .filter(Q(quiz__quizprops__name='\"courseversion\"') 
            | Q(quiz__quizprops__name='\"moodle_quiz_id\"') ) \
            .values('id',
                    'user__id',
                    'user__username',
                    'user__first_name',
                    'user__last_name',
                    'user__email',
                    'user__userprofile__phone_number',
                    'user__userprofilecustomfield__key_name',
                    'user__userprofilecustomfield__value_int',
                    'user__userprofilecustomfield__value_str',
                    'user__userprofilecustomfield__value_bool',
                    'quiz__title',
                    'quiz__quizprops__name',
                    'quiz__quizprops__value',
                    'attempt_date',
                    'score',
                    'maxscore') \
            .annotate(
                score_percent=F(
                    'score') / F(
                    'maxscore') * 100)
        print(qs.query)

        return str(qs.query)
