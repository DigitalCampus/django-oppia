# integrations/dhis/views.py
import json
import tablib

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.shortcuts import render 
from django.utils.translation import ugettext_lazy as _

@staff_member_required
def export(request):
    
    headers = ('username', 
               'month',
               'year',
               'activities_completed',
               'points_earned',
               'quizzes_passed')
    
    data = []
    data = tablib.Dataset(*data, headers=headers)
    
    response = HttpResponse(data.csv, content_type='application/text;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=dhis-export.csv" 

    return response