# oppia/views.py

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render

from oppia.models import Activity
from oppia.permissions import check_owner
from oppia.views.utils import quiz_attempts_pagination
from quiz.models import Quiz, QuizAttempt, QuizAttemptResponse


def course_quiz(request, course_id):
    course = check_owner(request, course_id)
    digests = Activity.objects.filter(section__course=course,
                                      type='quiz') \
        .order_by('section__order').distinct()
    quizzes = []
    for d in digests:
        try:
            quizobjs = Quiz.objects.filter(quizprops__name='digest',
                                           quizprops__value=d.digest)
            if len(quizobjs) > 0:
                q = quizobjs[0]
                q.section_name = d.section.title
                quizzes.append(q)
        except Quiz.DoesNotExist:
            pass
    return render(request, 'course/quizzes.html',
                  {'course': course,
                   'quizzes': quizzes})


def course_quiz_attempts(request, course_id, quiz_id):
    # get the quiz digests for this course
    course, quiz, attempts = quiz_attempts_pagination(request,
                                                      course_id,
                                                      quiz_id)

    return render(request, 'course/quiz-attempts.html',
                  {'course': course,
                   'quiz': quiz,
                   'page': attempts})


def course_feedback(request, course_id):
    course = check_owner(request, course_id)
    digests = Activity.objects.filter(section__course=course,
                                      type='feedback') \
        .order_by('section__order').values('digest').distinct()
    feedback = []
    for d in digests:
        quizobjs = Quiz.objects.filter(quizprops__name='digest',
                                       quizprops__value=d['digest'])
        if len(quizobjs) > 0:
            q = quizobjs[0]
            feedback.append(q)

    return render(request, 'course/feedback.html',
                  {'course': course,
                   'feedback': feedback})


def course_feedback_responses(request, course_id, quiz_id):
    # get the quiz digests for this course
    course, quiz, attempts = quiz_attempts_pagination(request,
                                                      course_id,
                                                      quiz_id)

    return render(request, 'course/feedback-responses.html',
                  {'course': course,
                   'quiz': quiz,
                   'page': attempts})
