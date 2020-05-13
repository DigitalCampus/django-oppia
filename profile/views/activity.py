import datetime
import operator
from itertools import chain

from django.db.models import Max, Min, Avg
from django.shortcuts import render
from django.utils import timezone

from oppia.models import Activity
from oppia.permissions import get_user, \
    get_user_courses, \
    can_view_course
from profile.views.utils import get_tracker_activities
from quiz.models import Quiz, QuizAttempt
from reports.signals import dashboard_accessed
from summary.models import UserCourseSummary


def user_activity(request, user_id):

    view_user = get_user(request, user_id)

    dashboard_accessed.send(sender=None, request=request, data=None)

    cohort_courses, other_courses, all_courses = get_user_courses(request,
                                                                  view_user)

    courses = []
    for course in all_courses:
        course_stats = UserCourseSummary.objects.filter(user=view_user,
                                                        course=course)
        if course_stats:
            course_stats = course_stats[0]
            data = {'course': course,
                    'course_display': str(course),
                    'no_quizzes_completed': course_stats.quizzes_passed,
                    'pretest_score': course_stats.pretest_score,
                    'no_activities_completed':
                        course_stats.completed_activities,
                    'no_media_viewed': course_stats.media_viewed,
                    'no_points': course_stats.points,
                    'no_badges': course_stats.badges_achieved, }
        else:
            data = {'course': course,
                    'course_display': str(course),
                    'no_quizzes_completed': 0,
                    'pretest_score': None,
                    'no_activities_completed': 0,
                    'no_media_viewed': 0,
                    'no_points': 0,
                    'no_badges': 0, }

        courses.append(data)

    order_options = ['course_display',
                     'no_quizzes_completed',
                     'pretest_score',
                     'no_activities_completed',
                     'no_points',
                     'no_badges',
                     'no_media_viewed']
    default_order = 'course_display'

    ordering = request.GET.get('order_by', default_order)
    inverse_order = ordering.startswith('-')
    if inverse_order:
        ordering = ordering[1:]

    if ordering not in order_options:
        ordering = default_order
        inverse_order = False

    courses.sort(key=operator.itemgetter(ordering), reverse=inverse_order)

    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()

    course_ids = list(chain(cohort_courses.values_list('id', flat=True),
                            other_courses.values_list('id', flat=True)))
    activity = get_tracker_activities(start_date,
                                      end_date,
                                      view_user,
                                      course_ids=course_ids)

    return render(request, 'profile/user-scorecard.html',
                  {'view_user': view_user,
                   'courses': courses,
                   'page_ordering': ('-' if inverse_order else '') + ordering,
                   'activity_graph_data': activity})


def user_course_activity_view(request, user_id, course_id):

    view_user = get_user(request, user_id)

    dashboard_accessed.send(sender=None, request=request, data=None)
    course = can_view_course(request, course_id)

    act_quizzes = Activity.objects \
        .filter(section__course=course, type=Activity.QUIZ) \
        .order_by('section__order', 'order')

    quizzes_attempted = 0
    quizzes_passed = 0
    course_pretest = None

    quizzes = []
    for aq in act_quizzes:
        quiz, course_pretest, quizzes_attempted, quizzes_passed = \
            process_quiz_activity(view_user,
                                  aq,
                                  course_pretest,
                                  quizzes_attempted,
                                  quizzes_passed)
        quizzes.append(quiz)

    activities_completed = course.get_activities_completed(course, view_user)
    activities_total = course.get_no_activities()
    activities_percent = (activities_completed * 100) / activities_total

    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()

    activity = get_tracker_activities(start_date,
                                      end_date,
                                      view_user,
                                      course=course)

    order_options = ['quiz_order',
                     'no_attempts',
                     'max_score',
                     'min_score',
                     'first_score',
                     'latest_score',
                     'avg_score']
    default_order = 'quiz_order'
    ordering = request.GET.get('order_by', default_order)
    inverse_order = ordering.startswith('-')
    if inverse_order:
        ordering = ordering[1:]
    if ordering not in order_options:
        ordering = default_order
        inverse_order = False

    quizzes.sort(key=operator.itemgetter(ordering), reverse=inverse_order)

    return render(request, 'profile/user-course-scorecard.html',
                  {'view_user': view_user,
                   'course': course,
                   'quizzes': quizzes,
                   'quizzes_passed': quizzes_passed,
                   'quizzes_attempted': quizzes_attempted,
                   'pretest_score': course_pretest,
                   'activities_completed': activities_completed,
                   'activities_total': activities_total,
                   'activities_percent': activities_percent,
                   'page_ordering': ('-' if inverse_order else '') + ordering,
                   'activity_graph_data': activity})


def process_quiz_activity(view_user,
                          aq,
                          course_pretest,
                          quizzes_attempted,
                          quizzes_passed):
    quiz = Quiz.objects.filter(quizprops__value=aq.digest,
                               quizprops__name="digest").first()

    no_attempts = quiz.get_no_attempts_by_user(quiz, view_user)
    attempts = QuizAttempt.objects.filter(quiz=quiz, user=view_user)

    passed = False
    if no_attempts > 0:
        quiz_maxscore = float(attempts[0].maxscore)
        attemps_stats = attempts.aggregate(max=Max('score'),
                                           min=Min('score'),
                                           avg=Avg('score'))
        max_score = 100 * float(attemps_stats['max']) / quiz_maxscore
        min_score = 100 * float(attemps_stats['min']) / quiz_maxscore
        avg_score = 100 * float(attemps_stats['avg']) / quiz_maxscore
        first_date = attempts \
            .aggregate(date=Min('attempt_date'))['date']
        recent_date = attempts \
            .aggregate(date=Max('attempt_date'))['date']
        first_score = 100 * float(attempts
                                  .filter(attempt_date=first_date)[0]
                                  .score) / quiz_maxscore
        latest_score = 100 * float(attempts
                                   .filter(attempt_date=recent_date)[0]
                                   .score) / quiz_maxscore

        passed = max_score is not None and max_score > 75
        if quiz.is_baseline():
            course_pretest = first_score
        else:
            quizzes_attempted += 1
            quizzes_passed = (quizzes_passed + 1) \
                if passed else quizzes_passed

    else:
        max_score = None
        min_score = None
        avg_score = None
        first_score = None
        latest_score = None

    quiz = {'quiz': aq,
            'id': quiz.pk if quiz else None,
            'quiz_order': aq.order,
            'no_attempts': no_attempts,
            'max_score': max_score,
            'min_score': min_score,
            'first_score': first_score,
            'latest_score': latest_score,
            'avg_score': avg_score,
            'passed': passed
            }
    return quiz, course_pretest, quizzes_attempted, quizzes_passed
