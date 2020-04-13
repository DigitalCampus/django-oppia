from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from tastypie.models import ApiKey

from urllib.parse import urlparse

from oppia import emailer
from oppia.models import Points, Award, Tracker
from oppia.permissions import can_edit_user
from profile.forms import LoginForm, \
    RegisterForm, \
    ResetForm, \
    ProfileForm
from profile.models import UserProfile, CustomField, UserProfileCustomField
from profile.views.utils import filter_redirect
from quiz.models import QuizAttempt, QuizAttemptResponse
from settings import constants
from settings.models import SettingProperties

STR_COMMON_FORM = 'common/form/form.html'
STR_OPPIA_HOME = 'oppia:index'


def login_view(request):
    username = password = ''

    # if already logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(STR_OPPIA_HOME))

    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = filter_redirect(request.POST)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if next is not None:
                parsed_uri = urlparse(next)
                if parsed_uri.netloc == '':
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(reverse(STR_OPPIA_HOME))
            else:
                return HttpResponseRedirect(reverse(STR_OPPIA_HOME))
    else:
        form = LoginForm(initial={'next': filter_redirect(request.GET), })

    return render(request, 'common/form/form.html',
                  {'username': username,
                   'form': form,
                   'title': _(u'Login')})


def register_form_process(form):
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

    # create UserProfile record
    user_profile = UserProfile()
    user_profile.user = user
    user_profile.job_title = form.cleaned_data.get("job_title")
    user_profile.organisation = form.cleaned_data.get("organisation")
    user_profile.save()

    # save any custom fields
    custom_fields = CustomField.objects.all()
    for custom_field in custom_fields:
        if custom_field.type == 'int':
            profile_field = UserProfileCustomField(
                key_name=custom_field,
                user=user,
                value_int=form.cleaned_data.get(custom_field.id))
        elif custom_field.type == 'bool':
            profile_field = UserProfileCustomField(
                key_name=custom_field,
                user=user,
                value_bool=form.cleaned_data.get(custom_field.id))
        else:
            profile_field = UserProfileCustomField(
                key_name=custom_field,
                user=user,
                value_str=form.cleaned_data.get(custom_field.id))
        if (form.cleaned_data.get(custom_field.id) is not None
            and form.cleaned_data.get(custom_field.id) != '') \
                or custom_field.required is True:
            profile_field.save()


def register(request):
    self_register = SettingProperties \
        .get_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                  settings.OPPIA_ALLOW_SELF_REGISTRATION)
    if not self_register:
        raise Http404

    if request.method == 'POST':  # if form submitted...
        form = RegisterForm(request.POST)
        if form.is_valid():  # All validation rules pass
            # Create new user
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            register_form_process(form)

            u = authenticate(username=username, password=password)
            if u is not None and u.is_active:
                login(request, u)
                return HttpResponseRedirect('thanks/')
    else:
        form = RegisterForm(initial={'next': filter_redirect(request.GET), })

    return render(request, STR_COMMON_FORM,
                  {'form': form,
                   'title': _(u'Register')})


def reset(request):
    if request.method == 'POST':  # if form submitted...
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

            emailer.send_oppia_email(
                template_html='profile/email/password_reset.html',
                template_text='profile/email/password_reset.txt',
                subject="Password reset",
                fail_silently=False,
                recipients=[user.email],
                new_password=newpass,
                site=prefix + request.META['SERVER_NAME']
                )

            return HttpResponseRedirect('sent/')
    else:
        form = ResetForm()  # An unbound form

    return render(request, STR_COMMON_FORM,
                  {'form': form,
                   'title': _(u'Reset password')})


def edit_form_initial(view_user, key):
    user_profile, created = UserProfile.objects \
        .get_or_create(user=view_user)

    initial = {'username': view_user.username,
               'email': view_user.email,
               'first_name': view_user.first_name,
               'last_name': view_user.last_name,
               'api_key': key.key,
               'job_title': user_profile.job_title,
               'organisation': user_profile.organisation}
    custom_fields = CustomField.objects.all()
    for custom_field in custom_fields:
        upcf_row = UserProfileCustomField.objects \
            .filter(key_name=custom_field, user=view_user)
        if upcf_row.exists():
            initial[custom_field.id] = upcf_row.first().get_value()

    return initial


def edit_form_process(form, view_user):
    email = form.cleaned_data.get("email")
    first_name = form.cleaned_data.get("first_name")
    last_name = form.cleaned_data.get("last_name")
    view_user.email = email
    view_user.first_name = first_name
    view_user.last_name = last_name
    view_user.save()

    user_profile, created = UserProfile.objects \
        .get_or_create(user=view_user)
    user_profile.job_title = form.cleaned_data.get("job_title")
    user_profile.organisation = form.cleaned_data.get("organisation")
    user_profile.save()

    # save any custom fields
    custom_fields = CustomField.objects.all()
    for custom_field in custom_fields:
        if (form.cleaned_data.get(custom_field.id) is not None
            and form.cleaned_data.get(custom_field.id) != '') \
                or custom_field.required is True:

            profile_field, created = UserProfileCustomField.objects \
                .get_or_create(key_name=custom_field, user=view_user)

            if custom_field.type == 'int':
                profile_field.value_int = \
                    form.cleaned_data.get(custom_field.id)
            elif custom_field.type == 'bool':
                profile_field.value_bool = \
                    form.cleaned_data.get(custom_field.id)
            else:
                profile_field.value_str = \
                    form.cleaned_data.get(custom_field.id)

            profile_field.save()


def edit(request, user_id=0):

    if user_id != 0 and can_edit_user(request, user_id):
        view_user = User.objects.get(pk=user_id)
    elif user_id == 0:
        view_user = request.user
    else:
        raise PermissionDenied

    key = ApiKey.objects.get(user=view_user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # update basic data
            edit_form_process(form, view_user)

            messages.success(request, _(u"Profile updated"))

            # if password should be changed
            password = form.cleaned_data.get("password")
            if password:
                view_user.set_password(password)
                view_user.save()
                messages.success(request, _(u"Password updated"))
    else:
        initial = edit_form_initial(view_user, key)
        form = ProfileForm(initial=initial)

    return render(request, 'profile/profile.html', {'form': form, 'user': view_user})


def export_mydata_view(request, data_type):
    if data_type == 'activity':
        my_activity = Tracker.objects.filter(user=request.user)
        return render(request, 'profile/export/activity.html',
                      {'activity': my_activity})
    elif data_type == 'quiz':
        my_quizzes = []
        my_quiz_attempts = QuizAttempt.objects.filter(user=request.user)
        for mqa in my_quiz_attempts:
            data = {}
            data['quizattempt'] = mqa
            data['quizattemptresponses'] = QuizAttemptResponse.objects \
                .filter(quizattempt=mqa)
            my_quizzes.append(data)

        return render(request, 'profile/export/quiz_attempts.html',
                      {'quiz_attempts': my_quizzes})
    elif data_type == 'points':
        points = Points.objects.filter(user=request.user)
        return render(request, 'profile/export/points.html',
                      {'points': points})
    elif data_type == 'badges':
        badges = Award.objects.filter(user=request.user)
        return render(request, 'profile/export/badges.html',
                      {'badges': badges})
    else:
        raise Http404


def points(request):
    points = Points.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(points, 25)  # Show 25 contacts per page

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
    return render(request, 'profile/points.html',
                  {'page': mypoints, })


def badges(request):
    awards = Award.objects.filter(user=request.user).order_by('-award_date')
    return render(request, 'profile/badges.html',
                  {'awards': awards, })
