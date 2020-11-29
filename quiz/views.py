import tablib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from oppia import constants
from oppia.models import Activity
from oppia.permissions import can_view_course_detail
from quiz.models import QuizProps, \
                        Question, \
                        QuizAttempt, \
                        QuizAttemptResponse

from reports.signals import dashboard_accessed


class FeedbackDownload(TemplateView):

    def get(self, request, course_id, feedback_id):

        activity = get_object_or_404(Activity,
                                     pk=feedback_id,
                                     type=Activity.FEEDBACK,
                                     section__course__pk=course_id)
        can_view_course_detail(request, course_id)

        dashboard_accessed.send(sender=None, request=request, data=None)

        prop = QuizProps.objects.get(name='digest', value=activity.digest)

        feedback_questions = Question.objects.filter(
            quizquestion__quiz__pk=prop.quiz_id) \
            .order_by('quizquestion__order')

        headers = ['Date', 'UserId']

        for question in feedback_questions:
            headers.append(question.get_title())

        data = []
        data = tablib.Dataset(* data, headers=headers)

        quiz_attempts = QuizAttempt.objects.filter(quiz_id=prop.quiz_id) \
            .order_by('attempt_date')

        for quiz_attempt in quiz_attempts:
            row = [quiz_attempt.attempt_date.strftime(
                constants.STR_DATETIME_FORMAT),
                   quiz_attempt.user_id]

            for question in feedback_questions:
                try:
                    user_response = QuizAttemptResponse.objects.get(
                        question=question,
                        quizattempt=quiz_attempt)
                    row.append(user_response.text)
                except QuizAttemptResponse.DoesNotExist:
                    row.append('')

            data.append(row)

        response = HttpResponse(
            data.export('xlsx'),
            content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=export.xlsx"

        return response


class QuizDownload(TemplateView):

    def get(self, request, course_id, quiz_id):
        activity = get_object_or_404(Activity,
                                     pk=quiz_id,
                                     type=Activity.QUIZ,
                                     section__course__pk=course_id)
        can_view_course_detail(request, course_id)

        prop = QuizProps.objects.get(name='digest', value=activity.digest)

        dashboard_accessed.send(sender=None, request=request, data=None)

        quiz_questions = Question.objects.filter(
            quizquestion__quiz__pk=prop.quiz_id) \
            .order_by('quizquestion__order')

        headers = ['Date', 'UserId', 'Max Score', 'User Score']

        for question in quiz_questions:
            headers.append(question.get_title())
            headers.append('Question Score')

        data = []
        data = tablib.Dataset(* data, headers=headers)

        quiz_attempts = QuizAttempt.objects.filter(quiz_id=prop.quiz_id) \
            .order_by('attempt_date')

        for quiz_attempt in quiz_attempts:
            row = [quiz_attempt.attempt_date.strftime(
                constants.STR_DATETIME_FORMAT),
                   quiz_attempt.user_id,
                   quiz_attempt.maxscore,
                   quiz_attempt.score]

            for question in quiz_questions:
                try:
                    user_response = QuizAttemptResponse.objects.get(
                        question=question,
                        quizattempt=quiz_attempt)
                    row.append(user_response.text)
                    row.append(user_response.score)
                except QuizAttemptResponse.DoesNotExist:
                    row.append('')
                    row.append('')

            data.append(row)

        response = HttpResponse(
            data.export('xlsx'),
            content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=export.xlsx"

        return response
