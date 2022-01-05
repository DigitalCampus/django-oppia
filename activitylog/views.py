import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, \
    HttpResponse, \
    HttpResponseBadRequest, HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from tastypie.models import ApiKey

from activitylog.forms import UploadActivityLogForm
from activitylog.models import UploadedActivityLog
from helpers.messages import MessagesDelegate
from oppia.permissions import user_can_upload
from api.resources.tracker import TrackerResource
from helpers.api.tasty_resource import create_resource
from profile.models import UserProfile
from quiz.api.resources import QuizAttemptResource

from django.views.generic import TemplateView

from settings import constants
from settings.models import SettingProperties


@method_decorator(user_can_upload, name='dispatch')
class UploadView(TemplateView):

    def get(self, request):
        form = UploadActivityLogForm()
        return render(request, 'common/upload.html',
                      {'form': form,
                       'title': _(u'Upload Activity Log')})

    def post(self, request):
        form = UploadActivityLogForm(request.POST, request.FILES)
        if form.is_valid():
            activity_log_file = request.FILES["activity_log_file"]

            # save activity_log_file
            uploaded_activity_log = \
                UploadedActivityLog(create_user=request.user,
                                    file=activity_log_file)
            uploaded_activity_log.save()

            # open file and process
            with open(uploaded_activity_log.file.path, 'rb') as file:
                file_data = file.read()
                messages_delegate = MessagesDelegate(request)
                success = process_activitylog(messages_delegate, file_data)
                if success:
                    return HttpResponseRedirect(
                        reverse('activitylog:upload_success'))

        return render(request, 'common/upload.html',
                      {'form': form,
                       'title': _(u'Upload Activity Log')})


def process_activitylog(messages_delegate, file_contents, messages=None):
    # open file and process
    json_data = json.loads(file_contents)
    if not validate_server(messages_delegate, json_data):
        return False
    else:
        process_uploaded_file(messages_delegate, json_data)
        return True


def process_uploaded_trackers(messages_delegate, trackers, user, user_api_key):

    request = HttpRequest()
    request.user = user
    for tracker in trackers:
        success, results = create_resource(TrackerResource, request, tracker)
        if success:
            messages_delegate.info(
                          _(u"Tracker activity %(uuid)s for %(username)s added"
                            % {'username': user.username, 'uuid': tracker.get('digest')}))
        else:
            messages_delegate.warning( _(
                u"Already uploaded: tracker activity %(uuid)s for %(username)s" % {'username': user.username,
                                       'uuid': tracker.get('digest', None)}),
                             'danger')


def process_uploaded_quizresponses(messages_delegate,
                                   quiz_responses,
                                   user,
                                   user_api_key):
    request = HttpRequest()
    request.user = user
    for quizattempt in quiz_responses:
        success, results = create_resource(QuizAttemptResource,
                                           request,
                                           quizattempt)
        if success:
            messages_delegate.info(_(u"Quiz attempt for %(username)s added"
                                     % {'username': user.username}))
        else:
            messages_delegate.info(
                          _(u"Already uploaded: quiz attempt for %(username)s added" % {'username': user.username}))


def process_uploaded_file(messages_delegate, json_data):
    if 'users' in json_data:
        for user in json_data['users']:
            username = user['username']
            req_user, user_profile = get_user_from_uploaded_log(messages_delegate, user)

            if 'job_title' in user and user['job_title'] != '':
                user_profile.job_title = user['job_title']
            if 'organisation' in user and user['organisation'] != '':
                user_profile.organisation = user['organisation']
            if 'phoneno' in user and user['phoneno'] != '':
                user_profile.phone_number = user['phoneno']
            user_profile.save()
            user_profile.update_customfields(user)

            try:
                user_api_key, created = ApiKey.objects \
                    .get_or_create(user=req_user)
                if (created):
                    messages_delegate.warning(
                                     _(u"Generated new ApiKey for \
                                       %(username)s : %(apikey)s" % {
                                           'username': username,
                                           'apikey': user_api_key.key}),
                                     'danger')

                if 'trackers' in user:
                    process_uploaded_trackers(messages_delegate,
                                              user['trackers'],
                                              req_user,
                                              user_api_key)
                if 'quizresponses' in user:
                    process_uploaded_quizresponses(messages_delegate,
                                                   user['quizresponses'],
                                                   req_user,
                                                   user_api_key)
            except ApiKey.DoesNotExist:
                messages_delegate.warning(
                                 _(u"%(username)s not found. Please \
                                   check that this file is being uploaded to \
                                   the correct server."
                                   % {'username': username}),
                                 'danger')


def get_user_from_uploaded_log(messages_delegate, user):
    username = user['username']

    for field in user:
        if user[field] == "null":
            user[field] = None

    if not User.objects.filter(username=username).exists():
        # User was registered offline, we create a new one
        req_user = User(
            username=username,
            email=user['email'] if user['email'] is not None else '',
        )

        req_user.password = user['password'] \
            if 'password' in user else make_password(None)
        req_user.first_name = user.get('firstname', '')
        req_user.last_name = user.get('lastname', '')
        req_user.save()

        user_profile = UserProfile(user=req_user)
        messages_delegate.warning(
                         _(u"%(username)s did not exist previously, and was created." % {'username': username}),
                         'danger')
    else:
        req_user = User.objects.filter(username=username).first()
        user_profile, created = UserProfile.objects.get_or_create(
            user=req_user)

    return req_user, user_profile


def validate_server(messages_delegate, data):

    if 'server' in data:
        server_url = SettingProperties.get_string(constants.OPPIA_HOSTNAME, "localhost")
        if data['server'].startswith(server_url):
            return True
        else:
            print('Different tracker server: {}'.format(data['server']))
            messages_delegate.warning(_(
                "The server in the activity log file does not match with the current one"))
            return False
    else:
        messages_delegate.warning(_(
            "The activity log file seems to be in a wrong format"))
        return False


@csrf_exempt
def post_activitylog(request):
    if request.method != 'PATCH':
        return HttpResponse(status=405)

    json.loads(request.body)

    messages_delegate = MessagesDelegate(request)
    success = process_activitylog(messages_delegate, request.body)
    if success:
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
