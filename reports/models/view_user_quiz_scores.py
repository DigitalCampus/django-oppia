from django.db.models import F, Q

from dbview.models import DbView

from quiz.models import QuizAttempt


class ViewUserQuizScores(DbView):

    @classmethod
    def view(cls):
        # for some reason the event and quizprops_name filters need to be
        # escaped - unclear why
        qs = QuizAttempt.objects.filter(
            user__is_staff=False,
            user__is_superuser=False,
            user__userprofile__exclude_from_reporting=False,
            event='\"quiz_attempt\"') \
            .filter(Q(quiz__quizprops__name='\"courseversion\"')
                    | Q(quiz__quizprops__name='\"moodle_quiz_id\"')) \
            .values('id',
                    userid=F('user__id'),
                    username=F('user__username'),
                    first_name=F('user__first_name'),
                    last_name=F('user__last_name'),
                    email=F('user__email'),
                    phone_number=F('user__userprofile__phone_number'),
                    profile_field_name=F('user__userprofilecustomfield__key_name'),
                    profile_field_value_int=F('user__userprofilecustomfield__value_int'),
                    profile_field_value_str=F('user__userprofilecustomfield__value_str'),
                    profile_field_value_bool=F('user__userprofilecustomfield__value_bool'),
                    quizid=F('quiz__id'),
                    quiz_title=F('quiz__title'),
                    quiz_property_name=F('quiz__quizprops__name'),
                    quiz_property_value=F('quiz__quizprops__value'),
                    quiz_attempt_date=F('attempt_date'),
                    user_score=F('score'),
                    quiz_maxscore=F('maxscore')) \
            .annotate(
                score_percent=F(
                    'user_score') / F(
                    'maxscore') * 100)

        return str(qs.query)
