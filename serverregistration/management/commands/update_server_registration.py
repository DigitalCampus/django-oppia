import datetime
import json
from urllib import request, parse
from urllib.error import HTTPError

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import ugettext as _

from oppia.models import Course

from settings import constants
from settings.models import SettingProperties


class Command(BaseCommand):
    help = 'Updates the Oppia server registration'

    OPPIA_IMPLEMENTATIONS_URL = "https://implementations.oppia-mobile.org/"
    NO_DAYS = 7

    NO_COURSES_KEY = "NO_COURSES"
    NO_USERS_KEY = "NO_USERS"

    def handle(self, *args, **options):

        # if server not registered then return
        if not SettingProperties.get_bool(constants.OPPIA_SERVER_REGISTERED,
                                          False):
            return

        # check when last sent, ignore if less than a week ago
        last_sent = SettingProperties.get_string(
            constants.OPPIA_SERVER_REGISTER_LAST_SENT, None)

        if last_sent is not None:
            start_date = datetime.datetime.now() - datetime.timedelta(
                days=self.NO_DAYS)
            last_sent_date = datetime.datetime.strptime(
                last_sent, constants.CRON_DATETIME_FORMAT)

        if last_sent is None or last_sent_date < start_date:        
            self.process_registration()

        # update last sent
        SettingProperties.set_string(constants.OPPIA_SERVER_REGISTER_LAST_SENT,
                                     timezone.now())

    def process_registration(self):

        # check if has api key or not
        api_key = SettingProperties.get_string(
                constants.OPPIA_SERVER_REGISTER_APIKEY,
                None)
        if api_key is None:
            api_key = self.get_api_key()

        if api_key:
            url = SettingProperties.get_string(
                constants.OPPIA_HOSTNAME,
                None)
            data_to_send = {'title': _(u'app_name'),
                            'server_url': url}

            if SettingProperties.get_bool(
                    constants.OPPIA_SERVER_REGISTER_EMAIL_NOTIF,
                    False):
                data_to_send['email_notifications'] = True
                data_to_send['email_notif_email'] = SettingProperties.get_string(
                    constants.OPPIA_SERVER_REGISTER_NOTIF_EMAIL_ADDRESS,
                    None)
            else:
                data_to_send['email_notifications'] = False

            statistics = {}
            if SettingProperties.get_bool(
                    constants.OPPIA_SERVER_REGISTER_NO_COURSES,
                    False):
                no_courses = Course.objects.all().count()
                statistics[self.NO_COURSES_KEY] = no_courses

            if SettingProperties.get_bool(
                    constants.OPPIA_SERVER_REGISTER_NO_USERS,
                    False):
                no_users = User.objects.all().count()
                statistics[self.NO_USERS_KEY] = no_users
  
            data_to_send['statistics'] = statistics

            url = self.OPPIA_IMPLEMENTATIONS_URL + "api/oppia/"

            data = bytes(json.dumps(data_to_send), encoding='utf-8')
            req =  request.Request(url, data=data) # this will make the method "POST"
            req.add_header('Content-Type', 'application/json')
            req.add_header('Authorization', 'Api-Key ' + api_key)

            request.urlopen(req)

    def get_api_key(self):
        try:
            url = self.OPPIA_IMPLEMENTATIONS_URL + "get-api-key/"
            req = request.Request(url)
            response = request.urlopen(req)
            api_key_data = json.loads(response.read())
            SettingProperties.set_string(
                    constants.OPPIA_SERVER_REGISTER_APIKEY,
                    api_key_data['key'])
            return api_key_data['key']
        except HTTPError:
            return None
