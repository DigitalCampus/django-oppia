# oppia/mobile/views.py
import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,render_to_response
from django.template import RequestContext

from oppia.models import Tracker, Points
from tastypie.authentication import ApiKeyAuthentication

def scorecard_view(request):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    start_date = datetime.datetime.now() - datetime.timedelta(days=14)
    end_date = datetime.datetime.now()
    media = {'views':Tracker.activity_views(user=request.user,type='media',start_date=start_date,end_date=end_date),
             'secs':Tracker.activity_secs(user=request.user,type='media',start_date=start_date,end_date=end_date),
             'points':Points.media_points(user=request.user,start_date=start_date,end_date=end_date)}
    quiz = {'views':Tracker.activity_views(user=request.user,type='quiz',start_date=start_date,end_date=end_date),
             'secs':Tracker.activity_secs(user=request.user,type='quiz',start_date=start_date,end_date=end_date),
             'points':Points.quiz_points(user=request.user,start_date=start_date,end_date=end_date)}
    acts = {'views':Tracker.activity_views(user=request.user,type='page',start_date=start_date,end_date=end_date),
             'secs':Tracker.activity_secs(user=request.user,type='page',start_date=start_date,end_date=end_date),
             'points':Points.page_points(user=request.user,start_date=start_date,end_date=end_date)}
    total = {'views':acts['views'] + quiz['views'] + media['views'],
             'secs': acts['secs'] + quiz['secs'] + media['secs'],
             'points': acts['points'] + quiz['points'] + media['points'],}
    scorecard = {'media':media, 'quiz':quiz, 'acts':acts, 'total': total}
    return render_to_response('oppia/mobile/scorecard.html',{ 'scorecard':scorecard }, context_instance=RequestContext(request))