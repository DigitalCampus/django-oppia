# integrations/dhis/views.py
import datetime
import dateutil.relativedelta
import tablib

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import render

from oppia.models import Tracker


@staff_member_required
def home(request):
    # get all the months/years that trackers exist for
    monthly_exports = Tracker.objects.all().datetimes('submitted_date',
                                                      'month',
                                                      'DESC')
    return render(request, 'integrations/dhis/index.html',
                  {'monthly_exports': monthly_exports})


@staff_member_required
def export_latest(request):
    last_month = datetime.datetime.now() \
        + dateutil.relativedelta.relativedelta(months=-1)
    data = create_csv(last_month.year, last_month.month)
    response = HttpResponse(data.csv,
                            content_type='application/text;charset=utf-8')
    response['Content-Disposition'] = \
        "attachment; filename=dhis-export-{year}-{month}.csv" \
        .format(year=last_month.year, month=last_month.month)

    return response


@staff_member_required
def export_month(request, year, month):
    data = create_csv(year, month)
    response = HttpResponse(data.csv,
                            content_type='application/text;charset=utf-8')
    response['Content-Disposition'] = \
        "attachment; filename=dhis-export-{year}-{month}.csv" \
        .format(year=year, month=month)

    return response


def create_csv(year, month):
    headers = ('username',
               'month',
               'year',
               'activities_completed',
               'points_earned',
               'quizzes_passed')

    data = []
    data = tablib.Dataset(*data, headers=headers)

    # get all the usernames for users who've had trackers or quizzes submitted
    users = Tracker.objects \
        .filter(submitted_date__month=month,
                submitted_date__year=year).values('user').distinct()

    for user in users:
        activities_completed = Tracker.objects \
            .filter(submitted_date__month=month,
                    submitted_date__year=year,
                    user__id=user['user'],
                    completed=True).count()
        points_earned = Tracker.objects \
            .filter(submitted_date__month=month,
                    submitted_date__year=year,
                    user__id=user['user']) \
            .aggregate(Sum('points'))['points__sum']
        quizzes_passed = Tracker.objects.filter(submitted_date__month=month,
                                                submitted_date__year=year,
                                                user__id=user['user'],
                                                completed=True,
                                                type='quiz').count()
        data.append(
                (
                    User.objects.get(pk=user['user']).username,
                    month,
                    year,
                    activities_completed,
                    points_earned,
                    quizzes_passed
                )
            )

    return data
