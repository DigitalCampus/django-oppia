# oppia/activitylog/views.py

import json
import urllib
import urllib2

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import exceptions
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from tastypie.models import ApiKey

from activitylog.forms import UploadActivityLogForm
from activitylog.models import UploadedActivityLog
from profile.models import UserProfile


def process_uploaded_trackers(request, user, user_api_key):
    for tracker in user['trackers']:
        url_comp = request.build_absolute_uri().split('/')
        url = ('%(protocol)s//%(domain)s/api/v1/tracker/?username=%(username)s&api_key=%(api_key)s' % {'protocol': url_comp[0], 'domain': url_comp[2], 'username': user['username'], 'api_key': user_api_key.key})
        data = json.dumps(tracker)
        req = urllib2.Request(url, data)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Accept', 'application/json; charset=utf-8')
        try:
            urllib2.urlopen(req)
            messages.info(request, _(u"Tracker activity for %(username)s added" % {'username': user['username']}))
        except urllib2.HTTPError:
            messages.warning(request, _(u"Already uploaded: tracker activity for %(username)s added" % {'username': user['username']}), 'danger')


def process_uploaded_quizresponses(request, user, user_api_key):
    for quizattempt in user['quizresponses']:
        url_comp = request.build_absolute_uri().split('/')
        url = ('%(protocol)s//%(domain)s/api/v1/quizattempt/?username=%(username)s&api_key=%(api_key)s' % {'protocol': url_comp[0], 'domain': url_comp[2], 'username': user['username'], 'api_key': user_api_key.key})
        data = json.dumps(quizattempt)
        req = urllib2.Request(url, data)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Accept', 'application/json; charset=utf-8')
        try:
            urllib2.urlopen(req)
            messages.info(request, _(u"Quiz attempt for %(username)s added" % {'username': user['username']}))
        except urllib2.HTTPError:
            messages.info(request, _(u"Already uploaded: quiz attempt for %(username)s added" % {'username': user['username']}))


def process_uploaded_file(request, json_data):
    if 'users' in json_data:
        for user in json_data['users']:
            username = user['username']
            print(_(u"processing activity log for %s" % username))

            if User.objects.filter(username=username).count() == 0:

                print(_(u"New user!"))
                # User was registered offline, we create a new one
                new_user = User(
                    username=username,
                    email=user['email'],
                )

                new_user.password = user['password'] if 'password' in user else make_password(None)
                new_user.first_name = user['firstname']
                new_user.last_name = user['lastname']
                new_user.save()

                user_profile = UserProfile()
                user_profile.user = new_user
                user_profile.phone_number = user['phoneno'] if 'phoneno' in user else None
                user_profile.job_title = user['jobtitle'] if 'jobtitle' in user else None
                user_profile.organisation = user['organisation'] if 'organisation' in user else None
                user_profile.save()

                messages.warning(request, _(
                    u"%(username)s did not exist previously, and was created." % {
                        'username': username}), 'danger')

            try:
                user_api_key, created = ApiKey.objects.get_or_create(user__username=username)
                if (created):
                    messages.warning(request, _(
                        u"Generated new ApiKey for %(username)s : %(apikey)s" % {
                            'username': username, 'apikey': user_api_key.key }), 'danger')

                if 'trackers' in user:
                    process_uploaded_trackers(request, user, user_api_key)
                if 'quizresponses' in user:
                    process_uploaded_quizresponses(request, user, user_api_key)
            except ApiKey.DoesNotExist:
                messages.warning(request, _(u"%(username)s not found. Please check that this file is being uploaded to the correct server." % {'username': username}), 'danger')
                print(_(u"No user api key found for %s" % user['username']))


def process_activitylog(request, contents):
    # open file and process
    json_data = json.loads(contents)
    if not validate_server(request, json_data):
        return False
    else:
        process_uploaded_file(request, json_data)
        return True


def validate_server(request, data):
    url_comp = request.build_absolute_uri().split('/')
    server_url = "%(protocol)s//%(domain)s" % ({'protocol': url_comp[0], 'domain': url_comp[2]})

    if 'server' in data and data['server'].startswith(server_url):
        print('Server check ok')
        return True
    else:
        print('Different tracker server: {}'.format(data['server']))
        messages.warning(request, _(
            "The server in the activity log file does not match with the current one"))
        return False

@csrf_exempt
def post_activitylog(request):
    if request.method != 'PATCH':
        return HttpResponse(status=405)

    json.loads(request.body)
    success = process_activitylog(request, request.body)
    if success:
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def upload_view(request):
    if not request.user.userprofile.get_can_upload_activitylog():
        raise exceptions.PermissionDenied

    if request.method == 'POST':
        form = UploadActivityLogForm(request.POST, request.FILES)
        if form.is_valid():
            activity_log_file = request.FILES["activity_log_file"]

            # save activity_log_file
            uploaded_activity_log = UploadedActivityLog(create_user=request.user,
                                      file=activity_log_file)
            uploaded_activity_log.save()

            # open file and process
            file_data = open(uploaded_activity_log.file.path, 'rb').read()
            success = process_activitylog(request, file_data)
            if success:
                return HttpResponseRedirect(reverse('oppia_activitylog_upload_success'))


    form = UploadActivityLogForm()
    return render(request, 'oppia/activitylog/upload.html',
                              {'form': form,
                               'title': _(u'Upload Activity Log')})
