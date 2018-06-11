# oppia/activitylog/views.py

import json
import urllib
import urllib2

from django.contrib import messages
from django.core import exceptions
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from tastypie.models import ApiKey

from oppia.activitylog.forms import UploadActivityLogForm
from oppia.activitylog.models import UploadedActivityLog

def process_uploaded_trackers(user, user_api_key):
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
 
def process_uploaded_quizresponses(user, user_api_key):
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
                                    
def process_uploaded_file(json_data):
    if 'users' in json_data:
        for user in json_data['users']:
            print(_(u"processing activity log for %s" % user['username']))
            try:
                user_api_key = ApiKey.objects.get(user__username=user['username'])
                if 'trackers' in user:
                    process_uploaded_trackers(user, user_api_key)
                if 'quizresponses' in user:
                    process_uploaded_quizresponses(user, user_api_key)
            except ApiKey.DoesNotExist:
                messages.warning(request, _(u"%(username)s not found. Please check that this file is being uploaded to the correct server." % {'username': user['username']}), 'danger')
                print(_(u"No user api key found for %s" % user['username']))
 
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
            json_data = json.loads(file_data)

            # TODO check server matches
            process_uploaded_file(json_data)
            
            return HttpResponseRedirect(reverse('oppia_activitylog_upload_success'))
    else:
        form = UploadActivityLogForm()

    return render(request, 'oppia/activitylog/upload.html',
                              {'form': form,
                               'title': _(u'Upload Activity Log')})
