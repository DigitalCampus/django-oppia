# oppia/mobile/views.py
import datetime
import oppia

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from oppia.models import Tracker, Points, Course, Cohort, CourseCohort, Participant, Activity, Section, Media
from oppia.quiz.models import Quiz, QuizAttempt, QuizAttemptResponse

from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import ApiKey


def scorecard_view(request):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)

    record_mobile_tracker(request, None, 'scorecard', '{"en":"homepage"}')

    start_date = datetime.datetime.now() - datetime.timedelta(days=14)
    end_date = datetime.datetime.now()
    media = {'views': Tracker.activity_views(user=request.user, type='media', start_date=start_date, end_date=end_date),
             'secs': Tracker.activity_secs(user=request.user, type='media', start_date=start_date, end_date=end_date),
             'points': Points.media_points(user=request.user, start_date=start_date, end_date=end_date)}
    quiz = {'views': Tracker.activity_views(user=request.user, type='quiz', start_date=start_date, end_date=end_date),
             'secs': Tracker.activity_secs(user=request.user, type='quiz', start_date=start_date, end_date=end_date),
             'points': Points.quiz_points(user=request.user, start_date=start_date, end_date=end_date)}
    acts = {'views': Tracker.activity_views(user=request.user, type='page', start_date=start_date, end_date=end_date),
             'secs': Tracker.activity_secs(user=request.user, type='page', start_date=start_date, end_date=end_date),
             'points': Points.page_points(user=request.user, start_date=start_date, end_date=end_date)}
    total = {'views': acts['views'] + quiz['views'] + media['views'],
             'secs': acts['secs'] + quiz['secs'] + media['secs'],
             'points': acts['points'] + quiz['points'] + media['points'], }
    scorecard = {'media': media, 'quiz': quiz, 'acts': acts, 'total': total}
    return render(request, 'oppia/mobile/scorecard.html', {'scorecard': scorecard})

def record_mobile_tracker(request, course_id, type, page):
    t = Tracker()
    t.user = request.user
    t.ip = request.META.get('REMOTE_ADDR', oppia.DEFAULT_IP_ADDRESS)
    t.agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    t.digest = ""
    t.data = ""
    t.course = course_id
    t.type = type
    t.completed = True
    t.activity_title = page
    t.save()
    return
