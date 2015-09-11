# oppia/profile/views.py
import csv
import datetime
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (authenticate, login, views)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from oppia.forms import DateRangeForm, DateRangeIntervalForm
from oppia.models import Points, Award, AwardCourse, Course, UserProfile, Tracker
from oppia.profile.forms import LoginForm, RegisterForm, ResetForm, ProfileForm, UploadProfileForm
from tastypie.models import ApiKey


def login_view(request):
    username = password = ''
    
    # if already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('oppia_home'))
    
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next')
        print next
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request,user)
            if next is not None:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('oppia_home'))
    else:
        form = LoginForm(initial={'next':request.GET.get('next'),})
        
    return render(request, 'oppia/form.html',{'username': username, 'form': form, 'title': _(u'Login')})

def register(request):
    if not settings.OPPIA_ALLOW_SELF_REGISTRATION:
        raise Http404
    
    if request.method == 'POST': # if form submitted...
        form = RegisterForm(request.POST)
        if form.is_valid(): # All validation rules pass
            # Create new user
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.job_title = form.cleaned_data.get("job_title")
            user_profile.organisation = form.cleaned_data.get("organisation")
            user_profile.save()
            u = authenticate(username=username, password=password)
            if u is not None:
                if u.is_active:
                    login(request, u)
                    return HttpResponseRedirect('thanks/')
            return HttpResponseRedirect('thanks/') # Redirect after POST
    else:
        form = RegisterForm(initial={'next':request.GET.get('next'),})

    return render(request, 'oppia/form.html', {'form': form, 'title': _(u'Register')})

def reset(request):
    if request.method == 'POST': # if form submitted...
        form = ResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                user = User.objects.get(email__exact=username)
            newpass = User.objects.make_random_password(length=8)
            user.set_password(newpass)
            user.save()
            if request.is_secure():
                prefix = 'https://'
            else:
                prefix = 'http://'
            # TODO - better way to manage email message content
            send_mail('OppiaMobile: Password reset', 'Here is your new password for OppiaMobile: '+newpass 
                      + '\n\nWhen you next log in you can update your password to something more memorable.' 
                      + '\n\n' + prefix + request.META['SERVER_NAME'] , 
                      settings.SERVER_EMAIL, [user.email], fail_silently=False)
            return HttpResponseRedirect('sent')
    else:
        form = ResetForm() # An unbound form

    return render(request, 'oppia/form.html', {'form': form,'title': _(u'Reset password')})

def edit(request):
    key = ApiKey.objects.get(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # update basic data
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            request.user.email = email
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.job_title = form.cleaned_data.get("job_title")
                user_profile.organisation = form.cleaned_data.get("organisation")
                user_profile.save()
            except UserProfile.DoesNotExist:
                user_profile = UserProfile()
                user_profile.user = request.user
                user_profile.job_title = form.cleaned_data.get("job_title")
                user_profile.organisation = form.cleaned_data.get("organisation")
                user_profile.save()
            messages.success(request, _(u"Profile updated"))
            
            # if password should be changed
            password = form.cleaned_data.get("password")
            if password:
                request.user.set_password(password)
                request.user.save()
                messages.success(request, _(u"Password updated"))
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile()
        form = ProfileForm(initial={'username':request.user.username,
                                    'email':request.user.email,
                                    'first_name':request.user.first_name,
                                    'last_name':request.user.last_name,
                                    'api_key': key.key,
                                    'job_title': user_profile.job_title,
                                    'organisation': user_profile.organisation,})
        
    return render(request, 'oppia/profile/profile.html', {'form': form,})

def points(request):
    points = Points.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(points, 25) # Show 25 contacts per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        mypoints = paginator.page(page)
    except (EmptyPage, InvalidPage):
        mypoints = paginator.page(paginator.num_pages)
    return render(request, 'oppia/profile/points.html', {'page': mypoints,})

def badges(request):
    awards = Award.objects.filter(user=request.user).order_by('-award_date')
    return render(request, 'oppia/profile/badges.html', {'awards': awards,})


def user_activity(request, user_id):
    if not request.user.is_staff:
        raise Http404
    
    user = User.objects.get(pk=user_id)
        
    start_date = datetime.datetime.now() - datetime.timedelta(days=31)
    end_date = datetime.datetime.now()
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")  
            start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
            end_date = form.cleaned_data.get("end_date")
            end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d") 
            trackers = Tracker.objects.filter(user=user,tracker_date__gte=start_date, tracker_date__lte=end_date).order_by('-tracker_date')
        else:
            trackers = Tracker.objects.filter(user=user).order_by('-tracker_date')             
    else:
        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        form = DateRangeForm(initial=data)
        trackers = Tracker.objects.filter(user=user).order_by('-tracker_date')
        
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
    
    return render_to_response('oppia/profile/user-activity.html',
                              {'user': user,
                               'form': form, 
                               'page':tracks,}, 
                              context_instance=RequestContext(request))

def upload_view(request):
    if not request.user.is_staff:
        raise Http404
    
    if request.method == 'POST': # if form submitted...
        form = UploadProfileForm(request.POST,request.FILES)
        if form.is_valid():
            request.FILES['upload_file'].open("rb")
            csv_file = csv.DictReader(request.FILES['upload_file'].file)
            required_fields = ['username','firstname','lastname','email']
            results = []
            try:
                for row in csv_file:
                    # check all required fields defined
                    all_defined = True
                    for rf in required_fields:
                        if rf not in row or row[rf].strip() == '':
                            result = {}
                            result['username'] = row['username']
                            result['created'] = False
                            result['message'] = _(u'No %s set' % rf)
                            results.append(result)
                            all_defined = False
                        
                    if not all_defined:    
                        continue
                    
                    user = User()
                    user.username = row['username']
                    user.first_name = row['firstname']
                    user.last_name = row['lastname']
                    user.email = row['email']
                    auto_password = False
                    if 'password' in row:
                        user.set_password(row['password'])
                    else:
                        password = User.objects.make_random_password()
                        user.set_password(password)
                        auto_password = True
                    try:
                        user.save()
                        up = UserProfile()
                        up.user = user
                        for col_name in row:
                            setattr(up, col_name, row[col_name])
                        up.save()
                        result = {}
                        result['username'] = row['username']
                        result['created'] = True
                        if auto_password:
                            result['message'] = _(u'User created with password: %s' % password)
                        else:
                            result['message'] = _(u'User created')
                        results.append(result)
                    except IntegrityError as ie:
                        result = {}
                        result['username'] = row['username']
                        result['created'] = False
                        result['message'] = _(u'User already exists')
                        results.append(result)
                        continue
            except:
                result = {}
                result['username'] = None
                result['created'] = False
                result['message'] = _(u'Could not parse file')
                results.append(result)
            
    else:
        results = []
        form = UploadProfileForm()
        
    return render(request, 'oppia/profile/upload.html', {'form': form, 'results': results})

def handle_profile_upload():
    pass