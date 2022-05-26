import datetime
import json
import operator
from itertools import chain

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Max, Min, Avg
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from helpers.mixins.DateRangeFilterMixin import DateRangeFilterMixin
from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from oppia.forms.activity_search import ActivitySearchForm
from oppia.models import Activity, Tracker
from oppia.permissions import get_user, get_user_courses, can_view_course, can_view_course_activity
from profile.views.utils import get_tracker_activities
from quiz.models import Quiz, QuizAttempt
from summary.models import UserCourseSummary


class UserScorecard(DateRangeFilterMixin, DetailView):
    template_name = 'profile/user-scorecard.html'
    context_object_name = 'view_user'
    pk_url_kwarg = 'user_id'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_user(self.request, self.object.pk) #TODO: Change permissions check
        cohort_courses, other_courses, all_courses = get_user_courses(self.request, self.object)

        courses = []
        for course in all_courses:
            course.can_view_course_activity = can_view_course_activity(self.request, course.id)
            courses.append(UserCourseSummary.objects.get_stats_summary(self.object, course))

        order_options = ['course_display',
                         'no_quizzes_completed',
                         'pretest_score',
                         'no_activities_completed',
                         'no_points',
                         'no_badges',
                         'no_media_viewed']
        default_order = 'course_display'

        ordering = self.request.GET.get('order_by', default_order)
        inverse_order = ordering.startswith('-')
        if inverse_order:
            ordering = ordering[1:]

        if ordering not in order_options:
            ordering = default_order
            inverse_order = False

        courses.sort(key=operator.itemgetter(ordering), reverse=inverse_order)

        start_date, end_date = self.get_daterange()
        course_ids = list(chain(cohort_courses.values_list('id', flat=True),
                                other_courses.values_list('id', flat=True)))
        activity = get_tracker_activities(start_date, end_date, self.object, course_ids=course_ids)

        context['courses'] = courses
        context['page_ordering'] = ('-' if inverse_order else '') + ordering
        context['activity_graph_data'] = activity
        return context


class UserCourseScorecard(DateRangeFilterMixin, DetailView):
    template_name = 'profile/user-course-scorecard.html'
    context_object_name = 'view_user'
    pk_url_kwarg = 'user_id'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        get_user(self.request, self.object.pk) #TODO: Change permissions check
        course = can_view_course(self.request, self.kwargs['course_id'])

        act_quizzes = Activity.objects \
            .filter(section__course=course, type=Activity.QUIZ) \
            .order_by('section__order', 'order')

        quizzes_attempted = 0
        quizzes_passed = 0
        course_pretest = None

        quizzes = []
        for aq in act_quizzes:
            quiz, course_pretest, quizzes_attempted, quizzes_passed = \
                process_quiz_activity(self.object, aq, course_pretest, quizzes_attempted, quizzes_passed)
            quizzes.append(quiz)

        activities_completed = course.get_activities_completed(course, self.object)
        activities_total = course.get_no_activities()
        activities_percent = (activities_completed * 100) / activities_total

        start_date, end_date = self.get_daterange()

        activity = get_tracker_activities(start_date, end_date, self.object, course=course)

        order_options = ['quiz_order',
                         'no_attempts',
                         'max_score',
                         'min_score',
                         'first_score',
                         'latest_score',
                         'avg_score']
        default_order = 'quiz_order'
        ordering = self.request.GET.get('order_by', default_order)
        inverse_order = ordering.startswith('-')
        if inverse_order:
            ordering = ordering[1:]
        if ordering not in order_options:
            ordering = default_order
            inverse_order = False

        quizzes.sort(key=operator.itemgetter(ordering), reverse=inverse_order)

        context['page_ordering'] = ('-' if inverse_order else '') + ordering
        context['course'] = course
        context['quizzes'] = quizzes
        context['quizzes_passed'] = quizzes_passed
        context['quizzes_attempted'] = quizzes_attempted
        context['pretest_score'] = course_pretest
        context['activities_completed'] = activities_completed
        context['activities_total'] = activities_total
        context['activities_percent'] = activities_percent
        context['activity_graph_data'] = activity

        return context


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


class UserActivityDetailList(DateRangeFilterMixin, SafePaginatorMixin, ListView):
    template_name = 'profile/activity/list.html'
    paginate_by = 25
    daterange_form_class = ActivitySearchForm

    def get_user_id(self):
        return self.kwargs['user_id']

    def get_queryset(self):
        self.filtered = False
        user = get_user(self.request, self.get_user_id())
        trackers = Tracker.objects.filter(user=user).exclude(type__exact='')

        start_date, end_date = self.get_daterange()

        print(start_date)
        print(end_date)
        trackers = trackers.filter( tracker_date__gte=start_date, tracker_date__lte=end_date)

        #filters = utils.get_filters_from_row(form, convert_date=False)
        #if filters:
        #    trackers = trackers.filter(**filters)
        #    self.filtered = True

        return trackers.order_by('-tracker_date')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_user(self.request, self.get_user_id())
        context['advanced_search'] = self.filtered

        for tracker in context['page_obj'].object_list:
            tracker.data_obj = []
            try:
                data_dict = json.loads(tracker.data)
                for key, value in data_dict.items():
                    tracker.data_obj.append([key, value])
            except ValueError:
                pass
            tracker.data_obj.append(['agent', tracker.agent])
            tracker.data_obj.append(['ip', tracker.ip])

        return context
