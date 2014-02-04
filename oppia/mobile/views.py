# oppia/mobile/views.py
import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,render_to_response, get_object_or_404
from django.template import RequestContext

from oppia.models import Tracker, Points, Course, Cohort, Participant, Activity, Section, Media
from oppia.quiz.models import Quiz, QuizAttempt, QuizAttemptResponse

from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import ApiKey

def scorecard_view(request):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    
    record_mobile_tracker(request,None,'scorecard','{"en":"homepage"}')
    
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
    
    record_mobile_tracker(request,None,'monitor','{"en":"homepage"}')
    
    # find courses this user is a teacher on
    now = datetime.datetime.now()
    cohorts = Cohort.objects.filter(participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    return render_to_response('oppia/mobile/monitor/home.html',{ 'cohorts_list':cohorts, 'user': request.user }, context_instance=RequestContext(request))


def monitor_cohort_progress_view(request,cohort_id):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    now = datetime.datetime.now()
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    cohort = get_object_or_404(Cohort, pk=cohort_id, participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    
    record_mobile_tracker(request,cohort.course,'monitor','{"en": "progress"}')
    
    sections = Section.objects.filter(course=cohort.course,order__gt=0).order_by('order')
    section_list = {}
    for s in sections:
        section_list[s.id] = Activity.objects.filter(section=s).values('digest').distinct()
    participants = Participant.objects.filter(cohort=cohort, role=Participant.STUDENT).order_by('user__first_name')
    
    paginator = Paginator(participants, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        students = paginator.page(page)
        for p in students:
            p.sections = []
            for s in sections:
                user_completed = Tracker.objects.filter(user=p.user,completed=True,digest__in=section_list[s.id]).values('digest').distinct()
                user_started = Tracker.objects.filter(user=p.user,completed=False,digest__in=section_list[s.id]).values('digest').distinct()
                temp = {'completed': user_completed.count()*100/section_list[s.id].count(), 
                        'started':user_started.count()*100/section_list[s.id].count(),
                        'section': s}
                p.sections.append(temp)
    except (EmptyPage, InvalidPage):
        tracks = paginator.page(paginator.num_pages)
        
    return render_to_response('oppia/mobile/monitor/progress.html',{ 'cohort':cohort, 'participants': students, 'user': request.user }, context_instance=RequestContext(request))


def monitor_cohort_quizzes_view(request,cohort_id):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    now = datetime.datetime.now()
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    cohort = get_object_or_404(Cohort, pk=cohort_id, participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    
    record_mobile_tracker(request,cohort.course,'monitor','{"en": "quizzes"}')
    
    quizzes = Activity.objects.filter(section__course=cohort.course,type='quiz').order_by('section__order')
    participants = Participant.objects.filter(cohort=cohort,role=Participant.STUDENT).order_by('user__first_name')
    
    paginator = Paginator(participants, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
      
    try:
        students = paginator.page(page)  
        for p in students:
            p.quizzes = []
            for quiz in quizzes:
                completed = False
                if Tracker.objects.filter(user=p.user, digest=quiz.digest,completed=True).count() > 0:
                    completed = True
                started = False
                if Tracker.objects.filter(user=p.user, digest=quiz.digest,completed=False).count() > 0:
                    started = True
                temp = { 'quiz': quiz,
                        'completed': completed,
                        'started': started}
                p.quizzes.append(temp)
    except (EmptyPage, InvalidPage):
        tracks = paginator.page(paginator.num_pages)
        
    return render_to_response('oppia/mobile/monitor/quizzes.html',{ 'cohort':cohort, 'participants': students, 'user': request.user }, context_instance=RequestContext(request))

def monitor_cohort_media_view(request,cohort_id):
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) is not True:
        return HttpResponse('Unauthorized', status=401)
    now = datetime.datetime.now()
    key = ApiKey.objects.get(user = request.user)
    request.user.key = key.key
    cohort = get_object_or_404(Cohort, pk=cohort_id, participant__user=request.user, participant__role=Participant.TEACHER, start_date__lte=now,end_date__gte=now)
    
    record_mobile_tracker(request,cohort.course,'monitor','{"en": "media"}')
    
    media = Media.objects.filter(course=cohort.course)
    participants = Participant.objects.filter(cohort=cohort,role=Participant.STUDENT).order_by('user__first_name')
    
    paginator = Paginator(participants, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
      
    try:
        students = paginator.page(page)
        for p in students:
            p.media = []
            for m in media:
                completed = False
                if Tracker.objects.filter(user=p.user, digest=m.digest,completed=True).count() > 0:
                    completed = True
                started = False
                if Tracker.objects.filter(user=p.user, digest=m.digest,completed=False).count() > 0:
                    started = True
                temp = { 'media': m,
                        'completed': completed,
                        'started': started}
                p.media.append(temp)
    except (EmptyPage, InvalidPage):
        tracks = paginator.page(paginator.num_pages)
        
    return render_to_response('oppia/mobile/monitor/media.html',{ 'cohort':cohort, 'participants': students, 'user': request.user }, context_instance=RequestContext(request))


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
    raise Http404

def record_mobile_tracker(request, course_id, type, page):
    t = Tracker()
    t.user = request.user
    t.ip = request.META.get('REMOTE_ADDR','0.0.0.0')
    t.agent = request.META.get('HTTP_USER_AGENT','unknown')
    t.digest = ""
    t.data = ""
    t.course = course_id
    t.type = type
    t.completed = True
    t.activity_title = page
    t.save()
    return
    
    
    