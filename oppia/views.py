# oppia/views.py
import datetime
import json
import shutil
import os
import oppia

from django import forms
from django.conf import settings
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.forms import UploadCourseForm, ScheduleForm
from oppia.forms import ActivityScheduleForm, CohortForm
from oppia.models import Course, Tracker, Tag, CourseTag, Schedule
from oppia.models import ActivitySchedule, Activity, Cohort, Participant, Points
from oppia.quiz.models import Quiz, QuizAttempt, QuizAttemptResponse

from uploader import handle_uploaded_file

def server_view(request):
    return render_to_response('oppia/server.html',  {'settings': settings}, content_type="application/json", context_instance=RequestContext(request))

def home_view(request):
    activity = []
    if request.user.is_authenticated():
        startdate = datetime.datetime.now()
        staff = User.objects.filter(is_staff=True)
        for i in range(31,-1,-1):
            temp = startdate - datetime.timedelta(days=i)
            day = temp.strftime("%d")
            month = temp.strftime("%m")
            year = temp.strftime("%y")
            count = Tracker.objects.filter(course__isnull=False, tracker_date__day=day,tracker_date__month=month,tracker_date__year=year).exclude(user_id__in=staff).count()
            activity.append([temp.strftime("%d %b %y"),count])
    leaderboard = Points.get_leaderboard(10)
    return render_to_response('oppia/home.html',{'recent_activity':activity, 'leaderboard':leaderboard}, context_instance=RequestContext(request))

def course_view(request):
    course_list = Course.objects.all().order_by('title')   
    startdate = datetime.datetime.now()
    staff = User.objects.filter(is_staff=True)
    for course in course_list:
        course.activity = []
        for i in range(7,-1,-1):
            temp = startdate - datetime.timedelta(days=i)
            day = temp.strftime("%d")
            month = temp.strftime("%m")
            year = temp.strftime("%y")
            count = Tracker.objects.filter(course = course, tracker_date__day=day,tracker_date__month=month,tracker_date__year=year).exclude(user_id__in=staff).count()
            course.activity.append([temp.strftime("%d %b %y"),count])   
    return render_to_response('oppia/course/course.html',{'course_list': course_list,}, context_instance=RequestContext(request))

       
def terms_view(request):
    return render_to_response('oppia/terms.html', {'settings': settings}, context_instance=RequestContext(request))
        
def upload(request):
    if settings.OPPIA_STAFF_ONLY_UPLOAD is True and not request.user.is_staff:
        return render_to_response('oppia/upload-staff-only.html', {'settings': settings}, context_instance=RequestContext(request))
        
    
    if request.method == 'POST':
        form = UploadCourseForm(request.POST,request.FILES)
        if form.is_valid(): # All validation rules pass
            extract_path = settings.COURSE_UPLOAD_DIR + 'temp/' + str(request.user.id) + '/' 
            course = handle_uploaded_file(request.FILES['course_file'], extract_path, request)
            if course:
                shutil.rmtree(extract_path)
                #add the tags
                tags = form.cleaned_data.get("tags").strip().split(",")
                if len(tags) > 0:
                    for t in tags:
                        try: 
                            tag = Tag.objects.get(name__iexact=t.strip())
                        except Tag.DoesNotExist:
                            tag = Tag()
                            tag.name = t.strip()
                            tag.created_by = request.user
                            tag.save()
                        # add tag to course
                        try:
                            ct = CourseTag.objects.get(course=course,tag=tag)
                        except CourseTag.DoesNotExist:
                            ct = CourseTag()
                            ct.course = course
                            ct.tag = tag
                            ct.save()
                return HttpResponseRedirect('success/') # Redirect after POST
            else:
                shutil.rmtree(extract_path,ignore_errors=True)
                os.remove(settings.COURSE_UPLOAD_DIR + request.FILES['course_file'].name)
    else:
        form = UploadCourseForm() # An unbound form

    return render(request, 'oppia/upload.html', {'form': form,})

def recent_activity(request,id):
    course = Course.objects.get(pk=id)
    dates = []
    startdate = datetime.datetime.now()
    staff = User.objects.filter(is_staff=True)
    for i in range(31,-1,-1):
        temp = startdate - datetime.timedelta(days=i)
        day = temp.strftime("%d")
        month = temp.strftime("%m")
        year = temp.strftime("%y")
        count_act_page = Tracker.objects.filter(course=course,type='page',tracker_date__day=day,tracker_date__month=month,tracker_date__year=year).exclude(user_id__in=staff).count()
        count_act_quiz = Tracker.objects.filter(course=course,type='quiz',tracker_date__day=day,tracker_date__month=month,tracker_date__year=year).exclude(user_id__in=staff).count()
        count_media = Tracker.objects.filter(course=course,type='media',tracker_date__day=day,tracker_date__month=month,tracker_date__year=year).exclude(user_id__in=staff).count()
        dates.append([temp.strftime("%d %b %y"),count_act_page,count_act_quiz,count_media])
    leaderboard = Points.get_leaderboard(10, course)
    return render_to_response('oppia/course/activity.html',{'course': course,'data':dates, 'leaderboard':leaderboard}, context_instance=RequestContext(request))

def recent_activity_detail(request,id):
    course = check_owner(request,id)
        
    staff = User.objects.filter(is_staff=True)
    trackers = Tracker.objects.filter(course=course).exclude(user_id__in=staff).order_by('-tracker_date')
    paginator = Paginator(trackers, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        tracks = paginator.page(page)
        for t in tracks:
            t.title = t.get_activity_title()   
            t.data_obj = []
            data_dict = json.loads(t.data)
            for key, value in data_dict.items():
                t.data_obj.append([key,value])
                       
    except (EmptyPage, InvalidPage):
        tracks = paginator.page(paginator.num_pages)
    return render_to_response('oppia/course/activity-detail.html',{'course': course,'page':tracks,}, context_instance=RequestContext(request))


def schedule(request,course_id):
    course = check_owner(request,course_id)    
    schedules = Schedule.objects.filter(course=course)
    return render_to_response('oppia/course/schedules.html',{'course': course,'schedules':schedules,}, context_instance=RequestContext(request))
    
def schedule_add(request,course_id):
    course = check_owner(request,course_id)
    ActivityScheduleFormSet = formset_factory(ActivityScheduleForm, extra=0)

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        formset = ActivityScheduleFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            schedule = Schedule()
            schedule.course = course
            schedule.title = form.cleaned_data.get("title").strip()
            schedule.default = form.cleaned_data.get("default")
            schedule.created_by = request.user
            
            # remvoe any existing default for this schedule
            if schedule.default:
                Schedule.objects.filter(course=course).update(default=False)
                
            schedule.save()
            
            for f in formset:
                act_sched = ActivitySchedule()
                start_date = f.cleaned_data.get("start_date")
                end_date = f.cleaned_data.get("end_date")
                digest = f.cleaned_data.get("digest")
                if start_date is not None:
                    act_sched = ActivitySchedule()
                    act_sched.schedule = schedule
                    act_sched.start_date = start_date
                    act_sched.end_date = end_date
                    act_sched.digest = digest.strip()
                    act_sched.save()
            return HttpResponseRedirect('../saved/')
    else:
        activities = Activity.objects.filter(section__course= course)
        initial = []
        section = None
        start_date = datetime.datetime.now() 
        end_date = datetime.datetime.now() + datetime.timedelta(days=7)
        for a in activities:
            if a.section != section:
                section = a.section
                start_date = start_date + datetime.timedelta(days=7)
                end_date = end_date + datetime.timedelta(days=7)
            data = {}
            data['title'] = a.title
            data['digest'] = a.digest
            data['section'] = a.section.title
            data['start_date'] = start_date
            data['end_date'] = end_date
            initial.append(data)
            form = ScheduleForm()
        formset = ActivityScheduleFormSet(initial=initial)

    return render(request, 'oppia/schedule-form.html', {'form': form, 'formset': formset,'course':course, })

def schedule_edit(request,course_id, schedule_id):
    course = check_owner(request,course_id)
    schedule = Schedule.objects.get(pk=schedule_id)
    ActivityScheduleFormSet = formset_factory(ActivityScheduleForm, extra=0)
    activities = Activity.objects.filter(section__course = course)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        formset = ActivityScheduleFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            schedule.title = form.cleaned_data.get("title").strip()
            schedule.default = form.cleaned_data.get("default")
            schedule.lastupdated_date = datetime.datetime.now()
            
            # remvoe any existing default for this schedule
            if schedule.default:
                Schedule.objects.filter(course=course).update(default=False)
                
            schedule.save()
            
            # remove all the old schedule Activities
            ActivitySchedule.objects.filter(schedule=schedule).delete()
            
            for f in formset:
                act_sched = ActivitySchedule()
                start_date = f.cleaned_data.get("start_date")
                end_date = f.cleaned_data.get("end_date")
                digest = f.cleaned_data.get("digest")
                if start_date is not None:
                    act_sched = ActivitySchedule()
                    act_sched.schedule = schedule
                    act_sched.start_date = start_date
                    act_sched.end_date = end_date
                    act_sched.digest = digest.strip()
                    act_sched.save()
            return HttpResponseRedirect('../saved/')
    else:
        initial = []
        section = None
        for a in activities:
            if a.section != section:
                section = a.section
            data = {}
            data['title'] = a.title
            data['digest'] = a.digest
            data['section'] = a.section.title
            try:
                act_s = ActivitySchedule.objects.get(schedule=schedule,digest = a.digest)
                start_date = act_s.start_date
                end_date = act_s.end_date
            except ActivitySchedule.DoesNotExist:
                start_date = None
                end_date = None
            data['start_date'] = start_date
            data['end_date'] = end_date
            initial.append(data)
        form = ScheduleForm(initial={'title':schedule.title,
                                    'default':schedule.default})
        formset = ActivityScheduleFormSet(initial=initial)

    return render(request, 'oppia/schedule-form.html', {'form': form, 'formset': formset,'course':course, })

def schedule_saved(request, course_id, schedule_id=None):
    course = check_owner(request,course_id)
    return render_to_response('oppia/schedule-saved.html', 
                                    {'course': course},
                                  context_instance=RequestContext(request))
 
def cohort(request,course_id):
    course = check_owner(request,course_id)    
    cohorts = Cohort.objects.filter(course=course)
    return render_to_response('oppia/course/cohorts.html',{'course': course,'cohorts':cohorts,}, context_instance=RequestContext(request))
  
def cohort_add(request,course_id):
    course = check_owner(request,course_id)
    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid(): # All validation rules pass
            cohort = Cohort()
            cohort.course = course
            cohort.start_date = form.cleaned_data.get("start_date")
            cohort.end_date = form.cleaned_data.get("end_date")
            cohort.description = form.cleaned_data.get("description").strip()
            cohort.save()
            
            students = form.cleaned_data.get("students").strip().split(",")
            if len(students) > 0:
                for s in students:
                    try:
                        student = User.objects.get(username=s.strip())
                        participant = Participant()
                        participant.cohort = cohort
                        participant.user = student
                        participant.role = Participant.STUDENT
                        participant.save()
                    except User.DoesNotExist:
                        pass
            teachers = form.cleaned_data.get("teachers").strip().split(",")
            if len(teachers) > 0:
                for t in teachers:
                    try:
                        teacher = User.objects.get(username=t.strip())
                        participant = Participant()
                        participant.cohort = cohort
                        participant.user = teacher
                        participant.role = Participant.TEACHER
                        participant.save()
                    except User.DoesNotExist:
                        pass
            return HttpResponseRedirect('../') # Redirect after POST
           
    else:
        form = CohortForm() # An unbound form

    return render(request, 'oppia/cohort-form.html',{'course': course,'form': form,})  

def cohort_edit(request,course_id,cohort_id):
    course = check_owner(request,course_id)
    cohort = Cohort.objects.get(pk=cohort_id)
    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid(): 
            cohort.description = form.cleaned_data.get("description").strip()
            cohort.start_date = form.cleaned_data.get("start_date")
            cohort.end_date = form.cleaned_data.get("end_date")
            cohort.save()
            
            Participant.objects.filter(cohort=cohort).delete()
            
            students = form.cleaned_data.get("students").split(",")
            if len(students) > 0:
                for s in students:
                    try:
                        participant = Participant()
                        participant.cohort = cohort
                        participant.user = User.objects.get(username=s.strip())
                        participant.role = Participant.STUDENT
                        participant.save()
                    except User.DoesNotExist:
                        pass
            teachers = form.cleaned_data.get("teachers").split(",")
            if len(teachers) > 0:
                for t in teachers:
                    try:
                        participant = Participant()
                        participant.cohort = cohort
                        participant.user = User.objects.get(username=t.strip())
                        participant.role = Participant.TEACHER
                        participant.save()
                    except User.DoesNotExist:
                        pass
            return HttpResponseRedirect('../../')
           
    else:
        participant_teachers = Participant.objects.filter(cohort=cohort,role=Participant.TEACHER)
        teacher_list = []
        for pt in participant_teachers:
            teacher_list.append(pt.user.username)
        teachers = ", ".join(teacher_list)
        
        participant_students = Participant.objects.filter(cohort=cohort,role=Participant.STUDENT)
        student_list = []
        for ps in participant_students:
            student_list.append(ps.user.username)
        students = ", ".join(student_list)
        form = CohortForm(initial={'description':cohort.description,'teachers':teachers,'students':students,'start_date': cohort.start_date,'end_date': cohort.end_date}) 

    return render(request, 'oppia/cohort-form.html',{'course': course,'form': form,}) 
         
def check_owner(request,id):
    try:
        # check only the owner can view 
        if request.user.is_staff:
            course = Course.objects.get(pk=id)
        else:
            course = Course.objects.get(pk=id,user=request.user)
    except Course.DoesNotExist:
        raise Http404
    return course

def leaderboard_view(request):
    lb = Points.get_leaderboard(100)
    paginator = Paginator(lb, 25) # Show 25 contacts per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        leaderboard = paginator.page(page)
    except (EmptyPage, InvalidPage):
        leaderboard = paginator.page(paginator.num_pages)

    return render_to_response('oppia/leaderboard.html',{'page':leaderboard}, context_instance=RequestContext(request))

def course_quiz(request,course_id):
    course = check_owner(request,course_id)
    digests = Activity.objects.filter(section__course=course,type='quiz').values('digest').distinct()
    quizzes = Quiz.objects.filter(quizprops__name='digest',quizprops__value__in=digests)
    
    return render_to_response('oppia/course/quizzes.html',{'course': course,'quizzes':quizzes}, context_instance=RequestContext(request))

def course_quiz_attempts(request,course_id,quiz_id):
    #get the quiz digests for this course
    course = check_owner(request,course_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    attempts = QuizAttempt.objects.filter(quiz=quiz).order_by('-attempt_date')
    
    paginator = Paginator(attempts, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        attempts = paginator.page(page)
        for a in attempts:
            a.responses = QuizAttemptResponse.objects.filter(quizattempt=a)                
    except (EmptyPage, InvalidPage):
        tracks = paginator.page(paginator.num_pages)
    
     
    return render_to_response('oppia/course/quiz-attempts.html',{'course': course,'quiz':quiz, 'page':attempts}, context_instance=RequestContext(request))