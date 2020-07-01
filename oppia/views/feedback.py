import tablib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from oppia.models import Activity
from oppia.permissions import can_view_course_detail
from quiz.models import Quiz, \
                        QuizProps, \
                        QuizQuestion, \
                        Question, \
                        QuizAttempt, \
                        QuizAttemptResponse


class FeedbackDownload(TemplateView):

    def get(self, request, course_id, feedback_id):
        can_view_course_detail(request, course_id)

        activity = get_object_or_404(Activity, pk=feedback_id)

        prop = QuizProps.objects.get(name='digest', value=activity.digest)

        feedback_questions = Question.objects.filter(
            quizquestion__quiz__pk=prop.quiz_id) \
            .order_by('quizquestion__order')

        print(prop.quiz.title)

        headers = ['Date',
               'UserId']

        for question in feedback_questions:
            headers.append(question.get_title())

        data = []
        data = tablib.Dataset(* data, headers=headers)

        quiz_attempts = QuizAttempt.objects.filter(quiz_id=prop.quiz_id) \
            .order_by('attempt_date')

        for quiz_attempt in quiz_attempts:
            row = [quiz_attempt.attempt_date.strftime('%Y-%m-%d %H:%M:%S'),
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