# oppia/reports/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.http.response import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from oppia.models import Course
from summary.models import UserCourseSummary


def menu_reports(request):
    # add in here any reports that need to appear in the menu
    # return [{'name': 'test',
    #            'url':'/reports/1/'},
    #         {'name': 'test2',
    #            'url':'/reports/2/'}]
    return [{'name': _('Completion Rates'),
             'url': reverse('reports:completion_rates')}]



@method_decorator(staff_member_required, name='dispatch')
class CompletionRates(TemplateView):

    def get(self, request):

        courses = Course.objects.filter(is_draft=False,
                                        is_archived=False).order_by('title')

        courses_list = []
        course_stats = list(UserCourseSummary.objects
                            .filter(course__in=courses)
                            .values('course')
                            .annotate(users=Count('user'),
                                      completed=Sum('badges_achieved')))

        for course in courses:
            obj = {}
            obj['course'] = course

            for stats in course_stats:
                if stats['course'] == course.id:
                    no_users = stats['users']
                    obj['enroled'] = no_users
                    if no_users > 0:
                        obj['completion'] = (float(stats['completed'])
                                             / float(no_users)) * 100
                    else:
                        obj['completion'] = 0
                    # remove the element to optimize next searches
                    course_stats.remove(stats)

            courses_list.append(obj)

        return render(request, 'reports/completion_rates.html',
                      {'courses_list': courses_list})



@method_decorator(staff_member_required, name='dispatch')
class CourseCompletionRates(TemplateView):

    def get(self, request, course_id):

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise Http404

        users_completed = []
        users_incompleted = []

        course_activities = course.get_no_activities()
        users_stats = UserCourseSummary.objects \
            .filter(course=course_id).order_by('user')

        for user_stats in users_stats:
            user_activities = user_stats.completed_activities
            user_obj = {'user': user_stats.user}
            user_obj['activities_completed'] = user_activities
            user_obj['completion_percent'] = (user_activities
                                              * 100
                                              / course_activities)
            if (user_activities >= course_activities):
                users_completed.append(user_obj)
            else:
                users_incompleted.append(user_obj)

        return render(request, 'reports/course_completion_rates.html',
                      {'course': course,
                       'users_enroled_count':
                       len(users_completed) + len(users_incompleted),
                       'users_completed': users_completed,
                       'users_incompleted': users_incompleted})
