import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from oppia.models import Course, Quiz, QuizAttempt
from oppia.permissions import check_owner
from quiz.models import QuizAttemptResponse


def quiz_attempts_pagination(request, course_id, quiz_id):
    course = check_owner(request, course_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    attempts = QuizAttempt.objects.filter(quiz=quiz).order_by('-attempt_date')

    paginator = Paginator(attempts, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        attempts = paginator.page(page)
        for a in attempts:
            a.responses = QuizAttemptResponse.objects.filter(quizattempt=a)
    except (EmptyPage, InvalidPage):
        paginator.page(paginator.num_pages)

    return course, quiz, attempts


def get_paginated_courses(request):
    default_order = 'lastupdated_date'
    ordering = request.GET.get('order_by', None)
    if ordering is None:
        ordering = default_order

    courses = Course.objects.all().order_by(ordering)
    paginator = Paginator(courses, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    return ordering, paginator.page(page)


def generate_graph_data(dates_types_stats, is_monthly=False):
    dates = []

    current_date = None
    current_stats = {}

    for date in dates_types_stats:
        if is_monthly:
            # depending if it is monthly or daily, we parse differently the
            # day "tag"
            day = datetime.date(month=date['month'], year=date['year'], day=1)
        else:
            day = date['day']

        if current_date is None or day != current_date:
            if current_date is not None:
                dates.append([current_date, current_stats])
            current_date = day
            current_stats = {'page': 0,
                             'quiz': 0,
                             'media': 0,
                             'resource': 0,
                             'total': 0}

        current_stats[date['type']] = date['total']
        current_stats['total'] += date['total']

    if current_date is not None:
        dates.append([current_date, current_stats])

    return dates
