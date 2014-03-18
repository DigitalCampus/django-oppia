# oppia/viz/views.py

import datetime
import json
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Sum

from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User

from oppia.viz.models import UserLocationVisualization


def summary_view(request):
    
    # User registrations
    user_registrations = User.objects.\
                        extra(select={'month':'extract( month from date_joined )',
                                      'year':'extract( year from date_joined )'}).\
                        values('month','year').\
                        annotate(count=Count('id')).order_by('year','month')
    
    # Countries
    country_activity =  UserLocationVisualization.objects.all().values('country').annotate(total_hits=Sum('hits')).order_by('-total_hits')
    
    
    return render_to_response('oppia/viz/summary.html',
                              {'user_registrations': user_registrations,
                               'country_activity': country_activity}, 
                              context_instance=RequestContext(request))
