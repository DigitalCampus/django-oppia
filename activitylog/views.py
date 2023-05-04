import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from tastypie.models import ApiKey

from activitylog.forms import UploadActivityLogForm
from activitylog.models import UploadedActivityLog
from api.resources.tracker import TrackerResource
from datarecovery.models import DataRecovery
from helpers.api.tasty_resource import create_resource
from helpers.messages import MessagesDelegate
from oppia.permissions import user_can_upload
from profile.models import UserProfile
from quiz.api.resources import QuizAttemptResource
from settings import constants
from settings.models import SettingProperties


@method_decorator(user_can_upload, name='dispatch')
class UploadView(FormView):

    form_class = UploadActivityLogForm
    template_name = 'common/upload.html'
    extra_context = {'title': _(u'Upload Activity Log')}
    success_url = reverse_lazy('activitylog:upload_success')

    def form_valid(self, form):
        activity_log_file = self.request.FILES["activity_log_file"]

        # save activity_log_file
        uploaded_activity_log = UploadedActivityLog(create_user=self.request.user, file=activity_log_file)
        uploaded_activity_log.save()

        # open file and process
        with open(uploaded_activity_log.file.path, 'rb') as file:
            file_data = file.read()
            messages_delegate = MessagesDelegate(self.request)
            success, errors = process_activitylog(messages_delegate, file_data)

        if success:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


def process_activitylog(messages_delegate, file_contents):
    # open file and process
    json_data = json.loads(file_contents)
    success, errors = validate_server(messages_delegate, json_data)
    if not success:
        return False, errors
    else:
        result, errors = process_uploaded_file(messages_delegate, json_data)
        return result, errors


def process_uploaded_trackers(messages_delegate, trackers, user):

    request = HttpRequest()
    request.user = user
    for tracker in trackers:
        success, results = create_resource(TrackerResource, request, tracker)
        if success:
            messages_delegate.info(
                          _(u"Tracker activity %(uuid)s for %(username)s added"
                            % {'username': user.username, 'uuid': tracker.get('digest')}))
        else:
            messages_delegate.warning(
                _(u"Already uploaded: tracker activity %(uuid)s for "
                  "%(username)s" % {'username': user.username, 'uuid': tracker.get('digest', None)}),
                'danger')


def process_uploaded_quizresponses(messages_delegate, quiz_responses, user):

    request = HttpRequest()
    request.user = user
    for quizattempt in quiz_responses:
        success, results = create_resource(QuizAttemptResource, request, quizattempt)
        if success:
            messages_delegate.info(_(u"Quiz attempt for %(username)s added"
                                     % {'username': user.username}))
        else:
            messages_delegate.info(
                _(u"Already uploaded: quiz attempt for %(username)s added" %
                  {'username': user.username}))


def process_uploaded_file(messages_delegate, json_data):
    errors = []
    if 'users' in json_data:
        for user in json_data['users']:
            username = user['username']
            req_user = get_user_from_uploaded_log(messages_delegate, user)
            user_profile_data = {data: user[data] for data in user if data not in ["username",
                                                                                   "trackers",
                                                                                   "quizresponses",
                                                                                   "points"]}
            errors = create_or_update_userprofile(messages_delegate, req_user, user_profile_data)

            try:
                user_api_key, created = ApiKey.objects.get_or_create(user=req_user)
                if (created):
                    messages_delegate.warning(
                         _(u"Generated new ApiKey for %(username)s : %(apikey)s" % {
                               'username': username,
                               'apikey': user_api_key.key}),
                         'danger')

                if 'trackers' in user:
                    process_uploaded_trackers(messages_delegate, user['trackers'], req_user)
                else:
                    errors.append(DataRecovery.Reason.MISSING_TRACKERS_TAG)
                    return False, errors
                if 'quizresponses' in user:
                    process_uploaded_quizresponses(messages_delegate, user['quizresponses'], req_user)
                else:
                    errors.append(DataRecovery.Reason.MISSING_QUIZRESPONSES_TAG)
                    return False, errors

            except ApiKey.DoesNotExist:
                messages_delegate.warning(
                     _(u"%(username)s not found. Please check that this file is being uploaded to \
                       the correct server." % {'username': username}), 'danger')
    else:
        errors.append(DataRecovery.Reason.MISSING_USER_TAG)
        return False, errors

    return True, errors


def get_user_from_uploaded_log(messages_delegate, user):
    username = user['username']

    for field in user:
        if user[field] == "null":
            user[field] = None

    if not User.objects.filter(username=username).exists():
        # User was registered offline, we create a new one
        req_user = User(username=username, email=user.get('email', ''))

        req_user.password = user.get('password', make_password(None))
        req_user.first_name = user.get('firstname', '')
        req_user.last_name = user.get('lastname', '')
        req_user.save()

        DataRecovery.create_data_recovery_entry(
            user=req_user,
            data_type=DataRecovery.Type.ACTIVITY_LOG,
            reasons=[DataRecovery.Reason.USER_DID_NOT_EXIST_AND_WAS_CREATED],
            data={'username': req_user.username, 'first_name': req_user.first_name, 'last_name': req_user.last_name}
        )

        messages_delegate.warning(
            _(u"%(username)s did not exist previously, and was created." % {'username': username}), 'danger')

    else:
        req_user = User.objects.filter(username=username).first()

    return req_user


def create_or_update_userprofile(messages_delegate, req_user, user_data):
    user_profile, created = UserProfile.objects.get_or_create(user=req_user)

    if 'job_title' in user_data and user_data['job_title']:
        user_profile.job_title = user_data['job_title']
    if 'organisation' in user_data and user_data['organisation']:
        user_profile.organisation = user_data['organisation']
    if 'phoneno' in user_data and user_data['phoneno']:
        user_profile.phone_number = user_data['phoneno']

    user_profile.save()
    errors = user_profile.update_customfields(user_data)
    return errors


def validate_server(messages_delegate, data):
    if 'server' in data:
        server_url = SettingProperties.get_string(constants.OPPIA_HOSTNAME, 'localhost')
        if data['server'].startswith(server_url):
            return True, None
        else:
            print('Different tracker server: {}'.format(data['server']))
            messages_delegate.warning(_('The server in the activity log file does not match with the current one'))
            return False, [DataRecovery.Reason.DIFFERENT_TRACKER_SERVER]
    else:
        messages_delegate.warning(_('The activity log file seems to be in a wrong format'))
        return False, [DataRecovery.Reason.MISSING_SERVER]


@csrf_exempt
# @deprecated - remove when API v2 is removed
def post_activitylog(request):
    if request.method != 'PATCH':
        return HttpResponse(status=405)

    json_data = json.loads(request.body)
    messages_delegate = MessagesDelegate(request)
    success, errors = process_activitylog(messages_delegate, request.body)

    users = []
    if 'users' in json_data:
        users = [user['username'] for user in json_data['users']]

    post_user = None
    for user in users:
        post_user = User.objects.filter(username=user).first()
        if post_user:
            break

    # If none of the users included exists in the server, we don't save the
    # file
    if post_user:
        username = users[0] if len(users) == 1 else 'activity'
        filename = '{}_{}.json'.format(username,
                                       timezone.now().strftime('%Y%m%d%H%M%S'))
        uploaded_activity_log = UploadedActivityLog(create_user=post_user)
        uploaded_activity_log.file.save(name=filename,
                                        content=ContentFile(request.body))
        uploaded_activity_log.save()
    else:
        errors.append(DataRecovery.Reason.NONE_OF_THE_INCLUDED_USERS_EXIST_ON_THE_SERVER)

    if errors:
        DataRecovery.create_data_recovery_entry(
            user=post_user,
            data_type=DataRecovery.Type.ACTIVITY_LOG,
            reasons=errors,
            data=json_data
        )

    if success:
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
