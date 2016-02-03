# oppia/views.py
import datetime
import json
import os
import oppia
import tablib

from dateutil.relativedelta import relativedelta

from django import forms
from django.conf import settings
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Q, Count
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.forms import UploadCourseStep1Form, UploadCourseStep2Form, ScheduleForm, DateRangeForm, DateRangeIntervalForm
from oppia.forms import ActivityScheduleForm, CohortForm
from oppia.models import Course, Tracker, Tag, CourseTag, Schedule, CourseManager, CourseCohort
from oppia.models import ActivitySchedule, Activity, Cohort, Participant, Points, UserProfile
from oppia.permissions import *
from oppia.quiz.models import Quiz, QuizAttempt, QuizAttemptResponse
from oppia.reports.signals import dashboard_accessed

from uploader import handle_uploaded_file

def server_view(request):
    return render_to_response('oppia/server.html',  
                              {'settings': settings}, 
                              content_type="application/json", 
                              context_instance=RequestContext(request))

def about_view(request):
    return render_to_response('oppia/about.html',  
                              {'settings': settings}, 
                              context_instance=RequestContext(request))
    
def home_view(request):
    activity = []
    if request.user.is_authenticated():
        # create profile if none exists (historical for very old users)
        try:
            up = request.user.userprofile
        except UserProfile.DoesNotExist:
            up = UserProfile()
            up.user= request.user
            up.save()
        
        dashboard_accessed.send(sender=None, request=request, data=None)
        
        # if user is student redirect to their scorecard
        if up.is_student_only():
            return HttpResponseRedirect(reverse('profile_user_activity', args=[request.user.id]))
        
        # is user is teacher redirect to teacher home
        if up.is_teacher_only():
            return HttpResponseRedirect(reverse('oppia_teacher_home'))
        
        start_date = timezone.now() - datetime.timedelta(days=31)
        end_date = timezone.now()
        interval = 'days'
        if request.method == 'POST':
            form = DateRangeIntervalForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data.get("start_date")  
                start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
                end_date = form.cleaned_data.get("end_date")
                end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")   
                interval =  form.cleaned_data.get("interval")          
        else:
            data = {}
            data['start_date'] = start_date
            data['end_date'] = end_date
            data['interval'] = interval
            form = DateRangeIntervalForm(initial=data)
        
        if interval == 'days':
            no_days = (end_date-start_date).days + 1
            trackers = Tracker.objects.filter(course__isnull=False, 
                                              course__is_draft=False, 
                                              user__is_staff=False, 
                                              course__is_archived=False,
                                              tracker_date__gte=start_date,
                                              tracker_date__lte=end_date).extra({'activity_date':"date(tracker_date)"}).values('activity_date').annotate(count=Count('id'))
            for i in range(0,no_days,+1):
                temp = start_date + datetime.timedelta(days=i)
                count = next((dct['count'] for dct in trackers if dct['activity_date'] == temp.date()), 0)
                activity.append([temp.strftime("%d %b %Y"),count])
        else:
            delta = relativedelta(months=+1)
            
            no_months = 0
            tmp_date = start_date
            while tmp_date <= end_date:
                print tmp_date
                tmp_date += delta
                no_months += 1
                
            for i in range(0,no_months,+1):
                temp = start_date + relativedelta(months=+i)
                month = temp.strftime("%m")
                year = temp.strftime("%Y")
                count = Tracker.objects.filter(course__isnull=False,
                                               course__is_draft=False,
                                               user__is_staff=False,
                                               course__is_archived=False,
                                               tracker_date__month=month,
                                               tracker_date__year=year).count()
                activity.append([temp.strftime("%b %Y"),count])
    else:
        form = None
    leaderboard = Points.get_leaderboard(10)
    return render_to_response('oppia/home.html',
                              {'form': form,
                               'activity_graph_data': activity, 
                               'leaderboard': leaderboard}, 
                              context_instance=RequestContext(request))

def teacher_home_view(request):
    cohorts, response = get_cohorts(request)
    if response is not None:
        return response
    
    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()
        
    # get student activity
    activity = []
    no_days = (end_date-start_date).days + 1
    students =  User.objects.filter(participant__role=Participant.STUDENT, participant__cohort__in=cohorts).distinct()   
    courses = Course.objects.filter(coursecohort__cohort__in=cohorts).distinct()
    trackers = Tracker.objects.filter(course__in=courses, 
                                       user__in=students,  
                                       tracker_date__gte=start_date,
                                       tracker_date__lte=end_date).extra({'activity_date':"date(tracker_date)"}).values('activity_date').annotate(count=Count('id'))
    for i in range(0,no_days,+1):
        temp = start_date + datetime.timedelta(days=i)
        count = next((dct['count'] for dct in trackers if dct['activity_date'] == temp.date()), 0)
        activity.append([temp.strftime("%d %b %Y"),count])
    
    return render_to_response('oppia/home-teacher.html',
                              {'cohorts': cohorts,
                               'activity_graph_data': activity, }, 
                              context_instance=RequestContext(request))

def courses_list_view(request):
    courses, response = can_view_courses_list(request) 
    if response is not None:
        return response
    
    dashboard_accessed.send(sender=None, request=request, data=None)
           
    tag_list = Tag.objects.all().exclude(coursetag=None).order_by('name')
    courses_list = []
    for course in courses:
        obj = {}
        obj['course'] = course
        access_detail, response = can_view_course_detail(request,course.id)
        if access_detail is not None:
            obj['access_detail'] = True
        else:
            obj['access_detail'] = False
        courses_list.append(obj)
        
    return render_to_response('oppia/course/courses-list.html',
                              {'courses_list': courses_list, 
                               'tag_list': tag_list}, 
                              context_instance=RequestContext(request))

def course_download_view(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404()
    file_to_download = course.getAbsPath();
    wrapper = FileWrapper(file(file_to_download))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Length'] = os.path.getsize(file_to_download)
    response['Content-Disposition'] = 'attachment; filename="%s"' %(course.filename)
    return response

def tag_courses_view(request, tag_id):
    courses, response = can_view_courses_list(request) 
    if response is not None:
        return response
    courses = courses.filter(coursetag__tag__pk=tag_id)
    
    dashboard_accessed.send(sender=None, request=request, data=None)
    
    courses_list = []
    for course in courses:
        obj = {}
        obj['course'] = course
        access_detail, response = can_view_course_detail(request,course.id)
        if access_detail is not None:
            obj['access_detail'] = True
        else:
            obj['access_detail'] = False
        courses_list.append(obj)
    tag_list = Tag.objects.all().order_by('name')
    return render_to_response('oppia/course/courses-list.html',
                              {'courses_list': courses_list, 
                               'tag_list': tag_list, 
                               'current_tag': id}, 
                              context_instance=RequestContext(request))
        
def upload_step1(request):
    if not request.user.userprofile.get_can_upload():
        return HttpResponse('Unauthorized', status=401)
        
    if request.method == 'POST':
        form = UploadCourseStep1Form(request.POST,request.FILES)
        if form.is_valid(): # All validation rules pass
            extract_path = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', str(request.user.id))
            course = handle_uploaded_file(request.FILES['course_file'], extract_path, request, request.user)
            if course:
                return HttpResponseRedirect(reverse('oppia_upload2', args=[course.id])) # Redirect after POST
            else:
                os.remove(settings.COURSE_UPLOAD_DIR + request.FILES['course_file'].name)
    else:
        form = UploadCourseStep1Form() # An unbound form

    return render_to_response('oppia/upload.html', 
                              {'form': form,
                               'title':_(u'Upload Course - step 1')},
                              context_instance=RequestContext(request))

def upload_step2(request, course_id):
    if not request.user.userprofile.get_can_upload():
        return HttpResponse('Unauthorized', status=401)
        
    course = Course.objects.get(pk=course_id)
    
    if request.method == 'POST':
        form = UploadCourseStep2Form(request.POST,request.FILES)
        if form.is_valid(): # All validation rules pass
            is_draft = form.cleaned_data.get("is_draft")
            if course:
                #add the tags
                tags = form.cleaned_data.get("tags").strip().split(",")
                is_draft = form.cleaned_data.get("is_draft")
                if len(tags) > 0:
                    course.is_draft = is_draft
                    course.save()
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
        form = UploadCourseStep2Form(initial={'tags':course.get_tags(),
                                    'is_draft':course.is_draft,}) # An unbound form

    return render_to_response('oppia/upload.html', 
                              {'form': form,
                               'title':_(u'Upload Course - step 2')},
                              context_instance=RequestContext(request))


def recent_activity(request,course_id):
    course, response = can_view_course_detail(request, course_id)
    
    if response is not None:
        return response
    
    dashboard_accessed.send(sender=None, request=request, data=course)
    
    start_date = datetime.datetime.now() - datetime.timedelta(days=31)
    end_date = datetime.datetime.now()
    interval = 'days'
    
    if request.method == 'POST':
        form = DateRangeIntervalForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")  
            start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
            end_date = form.cleaned_data.get("end_date")
            end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d") 
            interval =  form.cleaned_data.get("interval")               
    else:
        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['interval'] = interval
        form = DateRangeIntervalForm(initial=data)
    
    dates = []
    if interval == 'days':
        no_days = (end_date-start_date).days + 1
        
        for i in range(0,no_days,+1):
            temp = start_date + datetime.timedelta(days=i)
            day = temp.strftime("%d")
            month = temp.strftime("%m")
            year = temp.strftime("%Y")
            count_objs = Tracker.objects.filter(course=course,tracker_date__day=day,tracker_date__month=month,tracker_date__year=year).values('type').annotate(total=Count('type'))
            count_activity = {'page':0, 'quiz':0, 'media':0, 'resource':0, 'monitor': 0, 'total':0}
            for co in count_objs:
                if co['type'] in count_activity:
                    count_activity[co['type']] = count_activity[co['type']] + co['total']
                    count_activity['total'] = count_activity['total'] + co['total']
                else:
                    count_activity[co['type']] = 0
                    count_activity[co['type']] = count_activity[co['type']] + co['total']
                    count_activity['total'] = count_activity['total'] + co['total']
            
            dates.append([temp.strftime("%d %b %y"),count_activity])
    else:
        delta = relativedelta(months=+1)  
        no_months = 0
        tmp_date = start_date
        while tmp_date <= end_date:
            print tmp_date
            tmp_date += delta
            no_months += 1
            
        for i in range(0,no_months,+1):
            temp = start_date + relativedelta(months=+i)
            month = temp.strftime("%m")
            year = temp.strftime("%Y")
            count_objs = Tracker.objects.filter(course=course,tracker_date__month=month,tracker_date__year=year).values('type').annotate(total=Count('type'))
            count_activity = {'page':0, 'quiz':0, 'media':0, 'resource':0, 'monitor': 0, 'total':0}
            for co in count_objs:
                if co['type'] in count_activity:
                    count_activity[co['type']] = count_activity[co['type']] + co['total']
                    count_activity['total'] = count_activity['total'] + co['total']
                else:
                    count_activity[co['type']] = 0
                    count_activity[co['type']] = count_activity[co['type']] + co['total']
                    count_activity['total'] = count_activity['total'] + co['total']
            
            dates.append([temp.strftime("%b %y"),count_activity])
        
        
    leaderboard = Points.get_leaderboard(10, course)
    return render_to_response('oppia/course/activity.html',
                              {'course': course,
                               'form': form,
                                'data':dates, 
                                'leaderboard':leaderboard}, 
                              context_instance=RequestContext(request))

def recent_activity_detail(request,course_id):
    course, response = can_view_course_detail(request, course_id)
    
    if response is not None:
        return response
        
    start_date = datetime.datetime.now() - datetime.timedelta(days=31)
    end_date = datetime.datetime.now()
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")  
            start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
            end_date = form.cleaned_data.get("end_date")
            end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d") 
            trackers = Tracker.objects.filter(course=course,tracker_date__gte=start_date, tracker_date__lte=end_date).order_by('-tracker_date')
        else:
            trackers = Tracker.objects.filter(course=course).order_by('-tracker_date')             
    else:
        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        form = DateRangeForm(initial=data)
        trackers = Tracker.objects.filter(course=course).order_by('-tracker_date')
        
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
            t.data_obj = []
            try:
                data_dict = json.loads(t.data)
                for key, value in data_dict.items():
                    t.data_obj.append([key,value])
            except ValueError:
                pass
            t.data_obj.append(['agent',t.agent])
            t.data_obj.append(['ip',t.ip])
    except (EmptyPage, InvalidPage):
        tracks = paginator.page(paginator.num_pages)
    
    return render_to_response('oppia/course/activity-detail.html',
                              {'course': course,
                               'form': form, 
                               'page':tracks,}, 
                              context_instance=RequestContext(request))


def export_tracker_detail(request,course_id):
    course, response = can_view_course_detail(request, course_id)
    
    if response is not None:
        return response
    
    headers = ('Date', 'UserId', 'Type', 'Activity Title', 'Section Title', 'Time Taken', 'IP Address', 'User Agent', 'Language')
    data = []
    data = tablib.Dataset(*data, headers=headers)
    trackers = Tracker.objects.filter(course=course).order_by('-tracker_date')
    for t in trackers:
        try:
            data_dict = json.loads(t.data)
            if 'lang' in data_dict:
                lang = data_dict['lang']
            else:
                lang = ""
            data.append((t.tracker_date.strftime('%Y-%m-%d %H:%M:%S'), t.user.id, t.type, t.get_activity_title(), t.get_section_title(), t.time_taken, t.ip, t.agent, lang))
        except ValueError:
            data.append((t.tracker_date.strftime('%Y-%m-%d %H:%M:%S'), t.user.id, t.type, "", "", t.time_taken, t.ip, t.agent, ""))
            
    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=export.xls"

    return response
    
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
            
            # remove any existing default for this schedule
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
 
def cohort_list_view(request):
    if not request.user.is_staff:
        raise Http404  
    cohorts = Cohort.objects.all()
    return render_to_response('oppia/course/cohorts-list.html',
                              {'cohorts':cohorts,}, 
                              context_instance=RequestContext(request))
  
def cohort_add(request):
    if not can_add_cohort(request):
        return HttpResponse('Unauthorized', status=401)   
    
    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid(): # All validation rules pass
            cohort = Cohort()
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
             
            courses = form.cleaned_data.get("courses").strip().split(",")
            if len(courses) > 0:
                for c in courses:
                    try:
                        course = Course.objects.get(shortname=c.strip())
                        CourseCohort(cohort=cohort, course=course).save()
                    except Course.DoesNotExist:
                        pass
                           
            return HttpResponseRedirect('../') # Redirect after POST
           
    else:
        form = CohortForm() # An unbound form

    return render(request, 'oppia/cohort-form.html',{'form': form,})  

def cohort_view(request,cohort_id):
    cohort, response = can_view_cohort(request,cohort_id)
    
    if response is not None:
        return response
    
    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()
        
    # get student activity
    student_activity = []
    no_days = (end_date-start_date).days + 1
    students =  User.objects.filter(participant__role=Participant.STUDENT, participant__cohort=cohort)    
    trackers = Tracker.objects.filter(course__coursecohort__cohort=cohort, 
                                       user__is_staff=False,
                                       user__in=students,  
                                       tracker_date__gte=start_date,
                                       tracker_date__lte=end_date).extra({'activity_date':"date(tracker_date)"}).values('activity_date').annotate(count=Count('id'))
    for i in range(0,no_days,+1):
        temp = start_date + datetime.timedelta(days=i)
        count = next((dct['count'] for dct in trackers if dct['activity_date'] == temp.date()), 0)
        student_activity.append([temp.strftime("%d %b %Y"),count])
        
    # get leaderboard
    leaderboard = cohort.get_leaderboard(10)
    
    
    return render_to_response('oppia/course/cohort-activity.html',
                              {'cohort':cohort,
                               'activity_graph_data': student_activity, 
                               'leaderboard': leaderboard, }, 
                              context_instance=RequestContext(request))
    
def cohort_leaderboard_view(request,cohort_id):
    
    cohort, response = can_view_cohort(request,cohort_id)
    
    if cohort is None:
        return response
        
    # get leaderboard
    lb = cohort.get_leaderboard(0)
    
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

    
    return render_to_response('oppia/course/cohort-leaderboard.html',
                              {'cohort':cohort,
                               'page':leaderboard, }, 
                              context_instance=RequestContext(request))

def cohort_edit(request,cohort_id):
    if not can_edit_cohort(request, cohort_id):
        return HttpResponse('Unauthorized', status=401)  
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
             
            CourseCohort.objects.filter(cohort=cohort).delete()       
            courses = form.cleaned_data.get("courses").strip().split(",")
            if len(courses) > 0:
                for c in courses:
                    try:
                        course = Course.objects.get(shortname=c.strip())
                        CourseCohort(cohort=cohort, course=course).save()
                    except Course.DoesNotExist:
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
        
        cohort_courses = Course.objects.filter(coursecohort__cohort=cohort)
        course_list = []
        for c in cohort_courses:
            course_list.append(c.shortname)
        courses = ", ".join(course_list)
        
        form = CohortForm(initial={'description': cohort.description,
                                   'teachers': teachers,
                                   'students': students,
                                   'start_date': cohort.start_date,
                                   'end_date': cohort.end_date,
                                   'courses': courses}) 

    return render(request, 'oppia/cohort-form.html',{'form': form,}) 

def cohort_course_view(request, cohort_id, course_id): 
    cohort, response = can_view_cohort(request,cohort_id)
    if response is not None:
        return response
    
    try:
        course = Course.objects.get(pk=course_id, coursecohort__cohort=cohort)
    except Course.DoesNotExist:
        raise Http404()
    
    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()
    student_activity = []
    no_days = (end_date-start_date).days + 1
    users =  User.objects.filter(participant__role=Participant.STUDENT, participant__cohort=cohort).order_by('first_name', 'last_name')   
    trackers = Tracker.objects.filter(course=course, 
                                       user__is_staff=False,
                                       user__in=users,  
                                       tracker_date__gte=start_date,
                                       tracker_date__lte=end_date).extra({'activity_date':"date(tracker_date)"}).values('activity_date').annotate(count=Count('id'))
    for i in range(0,no_days,+1):
        temp = start_date + datetime.timedelta(days=i)
        count = next((dct['count'] for dct in trackers if dct['activity_date'] == temp.date()), 0)
        student_activity.append([temp.strftime("%d %b %Y"),count])
     
    students = []
    for user in users:
        data = {'user': user,
                'no_quizzes_completed': course.get_no_quizzes_completed(course,user),
                'pretest_score': course.get_pre_test_score(course,user),
                'no_activities_completed': course.get_activities_completed(course,user),
                'no_quizzes_completed': course.get_no_quizzes_completed(course,user),
                'no_points': course.get_points(course,user),
                'no_badges': course.get_badges(course,user),}
        students.append(data)
       
    return render_to_response('oppia/course/cohort-course-activity.html',
                              {'course': course,
                               'cohort': cohort, 
                               'activity_graph_data': student_activity,
                               'students': students }, 
                              context_instance=RequestContext(request))
       
def leaderboard_view(request):
    lb = Points.get_leaderboard()
    paginator = Paginator(lb, 25) # Show 25 per page

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

    return render_to_response('oppia/leaderboard.html',
                              {'page':leaderboard}, 
                              context_instance=RequestContext(request))

def course_quiz(request,course_id):
    course = check_owner(request,course_id)
    digests = Activity.objects.filter(section__course=course,type='quiz').order_by('section__order').distinct()
    quizzes = []
    for d in digests:
        try:
            q = Quiz.objects.get(quizprops__name='digest',quizprops__value=d.digest)
            q.section_name = d.section.title
            quizzes.append(q)
        except Quiz.DoesNotExist:
            pass
    return render_to_response('oppia/course/quizzes.html',
                              {'course': course, 
                               'quizzes':quizzes}, 
                              context_instance=RequestContext(request))

def course_quiz_attempts(request,course_id,quiz_id):
    # get the quiz digests for this course
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
    print  len(attempts)

    return render_to_response('oppia/course/quiz-attempts.html',
                              {'course': course,
                               'quiz':quiz, 
                               'page':attempts}, 
                              context_instance=RequestContext(request))

def course_feedback(request,course_id):
    course = check_owner(request,course_id)
    digests = Activity.objects.filter(section__course=course,type='feedback').order_by('section__order').values('digest').distinct()
    feedback = []
    for d in digests:
        try:
            q = Quiz.objects.get(quizprops__name='digest',quizprops__value=d['digest'])
            feedback.append(q)
        except Quiz.DoesNotExist:
            pass
        
    return render_to_response('oppia/course/feedback.html',
                              {'course': course,
                               'feedback':feedback}, 
                              context_instance=RequestContext(request))

def course_feedback_responses(request,course_id,quiz_id):
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

    return render_to_response('oppia/course/feedback-responses.html',
                              {'course': course,
                               'quiz':quiz, 
                               'page':attempts}, 
                              context_instance=RequestContext(request))