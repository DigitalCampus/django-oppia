# integrations/dhis/views.py
import json
import tablib

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.shortcuts import render 
from django.utils.translation import ugettext_lazy as _

from oppia.models import Tracker

@staff_member_required
def home(request):
    # get all the months/years that trackers exist for
    monthly_exports = Tracker.objects.all().datetimes('submitted_date', 'month', 'DESC')
    return render(request, 'integrations/dhis/index.html',
                  {'monthly_exports': monthly_exports})

@staff_member_required
def export_latest(request):
    data = create_csv(10, 2019)
    response = HttpResponse(data.csv, content_type='application/text;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=dhis-export-latest.csv" 

    return response

@staff_member_required
def export_month(request, year, month):
    data = create_csv(month, year)
    response = HttpResponse(data.csv, content_type='application/text;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=dhis-export.csv" 

    return response

def create_csv(month, year):
    headers = ('username', 
               'month',
               'year',
               'activities_completed',
               'points_earned',
               'quizzes_passed')
    
    data = []
    data = tablib.Dataset(*data, headers=headers)
    
    return data