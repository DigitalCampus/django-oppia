# oppia/mobile/views.py
import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,render_to_response, get_object_or_404
from django.template import RequestContext

from oppia.models import Tracker, Points, Course, Cohort, Participant, Activity, Section
from oppia.quiz.models import Quiz, QuizAttempt, QuizAttemptResponse

from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import ApiKey

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

def monitor_home_view(request):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    # find courses this user is a teacher on
    now = datetime.datetime.now()
    cohorts = Cohort.objects.filter(participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    return render_to_response('oppia/mobile/monitor/home.html',{ 'cohorts_list':cohorts, 'user': request.user }, context_instance=RequestContext(request))

def monitor_cohort_recent_view(request,cohort_id):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    now = datetime.datetime.now()
    cohort = get_object_or_404(Cohort, pk=cohort_id, participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    participants = Participant.objects.filter(cohort_id=cohort.id, role=Participant.STUDENT).order_by('user__first_name')
    start_date = datetime.datetime.now() - datetime.timedelta(days=14)
    end_date = datetime.datetime.now() 
    for p in participants:
        p.media = {'views':Tracker.activity_views(user=p.user,type='media',start_date=start_date,end_date=end_date, course=cohort.course),
                 'secs':Tracker.activity_secs(user=p.user,type='media',start_date=start_date,end_date=end_date, course=cohort.course),
                 'points':Points.media_points(user=p.user,start_date=start_date,end_date=end_date, course=cohort.course)}
        p.quiz = {'views':Tracker.activity_views(user=p.user,type='quiz',start_date=start_date,end_date=end_date, course=cohort.course),
                 'secs':Tracker.activity_secs(user=p.user,type='quiz',start_date=start_date,end_date=end_date, course=cohort.course),
                 'points':Points.quiz_points(user=p.user,start_date=start_date,end_date=end_date, course=cohort.course)}
        p.acts = {'views':Tracker.activity_views(user=p.user,type='page',start_date=start_date,end_date=end_date, course=cohort.course),
                 'secs':Tracker.activity_secs(user=p.user,type='page',start_date=start_date,end_date=end_date, course=cohort.course),
                 'points':Points.page_points(user=p.user,start_date=start_date,end_date=end_date, course=cohort.course)}  
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    
    return render_to_response('oppia/mobile/monitor/recent.html',{ 'cohort':cohort, 'participants': participants, 'user': request.user }, context_instance=RequestContext(request))
    

def monitor_cohort_overall_view(request,cohort_id):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    now = datetime.datetime.now()
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    cohort = get_object_or_404(Cohort, pk=cohort_id, participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    digests = Activity.objects.filter(section__course=cohort.course).values('digest').distinct()
    participants = Participant.objects.filter(cohort_id=cohort.id, role=Participant.STUDENT).order_by('user__first_name')
    for p in participants:
        user_completed = Tracker.objects.filter(user=p.user,completed=True,digest__in=digests).values('digest').distinct()
        p.completed = user_completed.count()*100/digests.count()
    return render_to_response('oppia/mobile/monitor/overall.html',{ 'cohort':cohort, 'participants': participants, 'user': request.user }, context_instance=RequestContext(request))


def monitor_cohort_quizzes_view(request,cohort_id):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    now = datetime.datetime.now()
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    cohort = get_object_or_404(Cohort, pk=cohort_id, participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    digests = Activity.objects.filter(section__course=cohort.course,type='quiz').values('digest').distinct()
    quizzes = Quiz.objects.filter(quizprops__name='digest',quizprops__value__in=digests)
    cohort_users = Participant.objects.filter(cohort=cohort,role=Participant.STUDENT).values('user__id').distinct()
    for q in quizzes:
        attempts = QuizAttempt.objects.filter(quiz=q, user__id__in=cohort_users)
        total = 0
        for a in attempts:
            total = total + a.get_score_percent()
        if attempts.count() > 0:
            avg_score = int(total/attempts.count())
        else:
            avg_score = 0
        q.attempts = attempts.count()
        q.average_score = avg_score
    return render_to_response('oppia/mobile/monitor/quizzes.html',{ 'cohort':cohort, 'quizzes': quizzes, 'user': request.user }, context_instance=RequestContext(request))

def monitor_cohort_student_view(request,cohort_id, student_id):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    now = datetime.datetime.now()
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    cohort = get_object_or_404(Cohort, pk=cohort_id, participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    raise Http404

def preview_course_home(request,course_id):
    
    return render_to_response('oppia/mobile/preview/home.html',{ 'user': request.user }, context_instance=RequestContext(request))
    
    
    