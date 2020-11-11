from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from oppia.models import Course

from reports.signals import dashboard_accessed

from summary.models import UserCourseSummary


@method_decorator(staff_member_required, name='dispatch')
class CourseCompletionRatesView(TemplateView):

    def get(self, request, course_id):
        dashboard_accessed.send(sender=None, request=request, data=None)
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
