# oppia/views.py
import datetime
import operator

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils import timezone

from oppia import constants
from oppia.forms.cohort import CohortForm
from oppia.models import Tracker, \
    CourseCohort, \
    Participant, \
    Course, \
    Cohort
from oppia.permissions import can_add_cohort, \
    can_view_cohort, \
    can_edit_cohort
from oppia.views.utils import get_paginated_courses, filter_trackers
from profile.views.utils import get_paginated_users
from summary.models import UserCourseSummary


def cohort_list_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    cohorts = Cohort.objects.all()
    return render(request, 'cohort/list.html', {'cohorts': cohorts, })


def cohort_add_roles(cohort, role, users):
    user_list = users.strip().split(",")
    for u in user_list:
        try:
            participant = Participant()
            participant.cohort = cohort
            participant.user = User.objects.get(username=u.strip())
            participant.role = role
            participant.save()
        except User.DoesNotExist:
            pass


def cohort_add_courses(cohort, courses):
    course_list = courses.strip().split(",")
    for c in course_list:
        try:
            course = Course.objects.get(shortname=c.strip())
            CourseCohort(cohort=cohort, course=course).save()
        except Course.DoesNotExist:
            pass


def cohort_add(request):
    if not can_add_cohort(request):
        raise PermissionDenied

    if request.method == 'POST':
        form = CohortForm(request.POST.copy())
        if form.is_valid():  # All validation rules pass
            cohort = Cohort()
            cohort.start_date = form.cleaned_data.get("start_date")
            cohort.end_date = form.cleaned_data.get("end_date")
            cohort.description = form.cleaned_data.get("description").strip()
            cohort.save()

            students = form.cleaned_data.get("students")
            cohort_add_roles(cohort, Participant.STUDENT, students)

            teachers = form.cleaned_data.get("teachers")
            cohort_add_roles(cohort, Participant.TEACHER, teachers)

            courses = form.cleaned_data.get("courses")
            cohort_add_courses(cohort, courses)

            return HttpResponseRedirect('../')  # Redirect after POST
        else:
            # If form is not valid, clean the groups data
            form.data['teachers'] = None
            form.data['courses'] = None
            form.data['students'] = None

    else:
        form = CohortForm()

    ordering, users = get_paginated_users(request)
    c_ordering, courses = get_paginated_courses(request)

    return render(request, 'cohort/form.html',
                  {'form': form,
                   'page': users,
                   'courses_page': courses,
                   'courses_ordering': c_ordering,
                   'page_ordering': ordering,
                   'users_list_template': 'select'})


def cohort_view(request, cohort_id):
    cohort = can_view_cohort(request, cohort_id)

    start_date = timezone.now() - datetime.timedelta(
        days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
    end_date = timezone.now()

    # get student activity
    students = User.objects.filter(participant__role=Participant.STUDENT,
                                   participant__cohort=cohort)
    trackers = Tracker.objects \
        .filter(course__coursecohort__cohort=cohort,
                user__is_staff=False,
                user__in=students)
    student_activity = filter_trackers(trackers, start_date, end_date)

    # get leaderboard
    leaderboard = cohort.get_leaderboard(
        constants.LEADERBOARD_HOMEPAGE_RESULTS_PER_PAGE)

    return render(request, 'cohort/activity.html',
                  {'cohort': cohort,
                   'activity_graph_data': student_activity,
                   'leaderboard': leaderboard, })


def cohort_leaderboard_view(request, cohort_id):

    cohort = can_view_cohort(request, cohort_id)

    # get leaderboard
    lb = cohort.get_leaderboard(0)

    paginator = Paginator(lb, constants.LEADERBOARD_TABLE_RESULTS_PER_PAGE)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        leaderboard = paginator.page(page)
    except (EmptyPage, InvalidPage):
        leaderboard = paginator.page(paginator.num_pages)

    return render(request, 'cohort/leaderboard.html',
                  {'cohort': cohort,
                   'page': leaderboard})


def cohort_edit(request, cohort_id):
    if not can_edit_cohort(request, cohort_id):
        raise PermissionDenied
    cohort = Cohort.objects.get(pk=cohort_id)
    teachers_selected = []
    students_selected = []
    courses_selected = []

    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid():
            cohort.description = form.cleaned_data.get("description").strip()
            cohort.start_date = form.cleaned_data.get("start_date")
            cohort.end_date = form.cleaned_data.get("end_date")
            cohort.save()

            Participant.objects.filter(cohort=cohort).delete()

            students = form.cleaned_data.get("students")
            cohort_add_roles(cohort, Participant.STUDENT, students)

            teachers = form.cleaned_data.get("teachers")
            cohort_add_roles(cohort, Participant.TEACHER, teachers)

            CourseCohort.objects.filter(cohort=cohort).delete()
            courses = form.cleaned_data.get("courses")
            cohort_add_courses(cohort, courses)

            return HttpResponseRedirect('../../')

    else:
        form = CohortForm(initial={'description': cohort.description,
                                   'start_date': cohort.start_date,
                                   'end_date': cohort.end_date})

    teachers_selected = User.objects.filter(
                          participant__role=Participant.TEACHER,
                          participant__cohort=cohort)
    students_selected = User.objects.filter(
                          participant__role=Participant.STUDENT,
                          participant__cohort=cohort)
    courses_selected = Course.objects.filter(coursecohort__cohort=cohort)

    ordering, users = get_paginated_users(request)
    c_ordering, courses = get_paginated_courses(request)

    return render(request, 'cohort/form.html',
                  {'form': form,
                   'page': users,
                   'selected_teachers': teachers_selected,
                   'selected_students': students_selected,
                   'selected_courses': courses_selected,
                   'courses_page': courses,
                   'courses_ordering': c_ordering,
                   'page_ordering': ordering,
                   'users_list_template': 'select'})


def cohort_course_view(request, cohort_id, course_id):
    cohort = can_view_cohort(request, cohort_id)

    try:
        course = Course.objects.get(pk=course_id, coursecohort__cohort=cohort)
    except Course.DoesNotExist:
        raise Http404()

    start_date = timezone.now() - datetime.timedelta(
            days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
    end_date = timezone.now()

    users = User.objects.filter(
        participant__role=Participant.STUDENT,
        participant__cohort=cohort).order_by('first_name', 'last_name')
    trackers = Tracker.objects.filter(course=course,
                                      user__is_staff=False,
                                      user__in=users)

    student_activity = filter_trackers(trackers, start_date, end_date)

    students = []
    media_count = course.get_no_media()
    for user in users:
        course_stats = UserCourseSummary.objects.filter(user=user,
                                                        course=course_id)
        if course_stats:
            course_stats = course_stats[0]
            if course_stats.pretest_score:
                pretest_score = course_stats.pretest_score
            else:
                pretest_score = 0
            data = {'user': user,
                    'user_display': str(user),
                    'no_quizzes_completed': course_stats.quizzes_passed,
                    'pretest_score': pretest_score,
                    'no_activities_completed':
                        course_stats.completed_activities,
                    'no_points': course_stats.points,
                    'no_badges': course_stats.badges_achieved,
                    'no_media_viewed': course_stats.media_viewed}
        else:
            # The user has no activity registered
            data = {'user': user,
                    'user_display': str(user),
                    'no_quizzes_completed': 0,
                    'pretest_score': 0,
                    'no_activities_completed': 0,
                    'no_points': 0,
                    'no_badges': 0,
                    'no_media_viewed': 0}

        students.append(data)

    order_options = ['user_display',
                     'no_quizzes_completed',
                     'pretest_score',
                     'no_activities_completed',
                     'no_points',
                     'no_badges',
                     'no_media_viewed']
    default_order = 'pretest_score'

    ordering = request.GET.get('order_by', default_order)
    inverse_order = ordering.startswith('-')
    if inverse_order:
        ordering = ordering[1:]

    if ordering not in order_options:
        ordering = default_order
        inverse_order = False

    students.sort(key=operator.itemgetter(ordering), reverse=inverse_order)

    return render(request, 'cohort/course-activity.html',
                  {'course': course,
                   'cohort': cohort,
                   'course_media_count': media_count,
                   'activity_graph_data': student_activity,
                   'page_ordering': ('-' if inverse_order else '') + ordering,
                   'students': students})
