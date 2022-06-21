import tablib
from django.db.models import Sum
from django.http import HttpResponse

from oppia.models import Course, User
from reports.views.base_report_template import BaseReportTemplateView
from summary.models import UserCourseDailySummary


class DownloadTimeSpentView(BaseReportTemplateView):

    def get(self, request, *args, **kwargs):
        start_date, end_date = self.get_daterange()
        data = self.get_graph_data(start_date, end_date)

        response = HttpResponse(data.csv, content_type='application/text;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=time_tracking.csv"
        return response


    def get_graph_data(self, start_date, end_date):

        headers = ('date',
                   'user_id',
                   'username',
                   'course',
                   'course_title',
                   'time_spent')
        data = []
        data = tablib.Dataset(*data, headers=headers)

        # get all the users who have some time spent in a day
        daily_summaries =  UserCourseDailySummary.objects\
            .values('day', 'user', 'course')\
            .annotate(time_spent=Sum('time_spent_tracked'))

        for aud in daily_summaries:

            print(aud)
            user = User.objects.filter(pk=aud['user']).first()
            course = Course.objects.filter(pk=aud['course']).first()
            data.append(
                        (
                           aud['day'],
                           aud['user'],
                           user.username,
                           course.shortname,
                           course.get_title(),
                           aud['time_spent']
                        )
                    )

        return data






