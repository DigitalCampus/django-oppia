import tablib
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from oppia import constants
from oppia.models import Activity
from oppia.permissions import can_view_course_detail
from quiz.models import QuizProps, \
    Question, \
    QuizAttempt, \
    QuizAttemptResponse, Quiz

STR_CONTENT_TYPE = 'application/vnd.ms-excel;charset=utf-8'
STR_CONTENT_DISPOSITION = "attachment; filename=export.xlsx"


def get_feedback_data(feedback_id):
    feedback_questions = Question.objects.filter(
        quizquestion__quiz__pk=feedback_id).order_by('quizquestion__order')
    headers = ['Date', 'UserId']

    for question in feedback_questions:
        headers.append(question.get_title())

    data = []
    data = tablib.Dataset(*data, headers=headers)

    quiz_attempts = QuizAttempt.objects.filter(quiz_id=feedback_id) \
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

    return data


def get_quiz_data(quiz_id):
    quiz_questions = Question.objects.filter(
        quizquestion__quiz__pk=quiz_id).order_by('quizquestion__order')

    headers = ['Date', 'UserId', 'Max Score', 'User Score']

    for question in quiz_questions:
        headers.append(question.get_title())
        headers.append('Question Score')

    data = []
    data = tablib.Dataset(*data, headers=headers)
    quiz_attempts = QuizAttempt.objects.filter(
        quiz_id=quiz_id).order_by('attempt_date')

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

    return data


def feedback_download(request, course_id, feedback_id):
    activity = get_object_or_404(Activity,
                                 pk=feedback_id,
                                 type=Activity.FEEDBACK,
                                 section__course__pk=course_id)
    can_view_course_detail(request, course_id)

    prop = QuizProps.objects.get(name=QuizProps.DIGEST, value=activity.digest)
    data = get_feedback_data(prop.quiz_id)

    response = HttpResponse(
        data.export('xlsx'),
        content_type=STR_CONTENT_TYPE)
    response['Content-Disposition'] = STR_CONTENT_DISPOSITION

    return response


def old_feedback_download(request, course_id, feedback_id):
    get_object_or_404(Quiz, pk=feedback_id)
    can_view_course_detail(request, course_id)

    data = get_feedback_data(feedback_id)

    response = HttpResponse(
        data.export('xlsx'),
        content_type=STR_CONTENT_TYPE)
    response['Content-Disposition'] = STR_CONTENT_DISPOSITION

    return response


def old_quiz_download(request, course_id, quiz_id):
    can_view_course_detail(request, course_id)
    get_object_or_404(Quiz, pk=quiz_id)

    quiz_data = get_quiz_data(quiz_id)
    response = HttpResponse(
        quiz_data.export('xlsx'),
        content_type=STR_CONTENT_TYPE)
    response['Content-Disposition'] = STR_CONTENT_DISPOSITION

    return response


def quiz_download(request, course_id, quiz_id):
    activity = get_object_or_404(Activity,
                                 pk=quiz_id,
                                 type=Activity.QUIZ,
                                 section__course__pk=course_id)
    can_view_course_detail(request, course_id)

    prop = QuizProps.objects.get(name=QuizProps.DIGEST, value=activity.digest)
    quiz_data = get_quiz_data(prop.quiz_id)

    response = HttpResponse(
        quiz_data.export('xlsx'),
        content_type=STR_CONTENT_TYPE)
    response['Content-Disposition'] = STR_CONTENT_DISPOSITION

    return response
