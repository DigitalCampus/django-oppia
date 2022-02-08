import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from oppia.models import Tracker


@method_decorator(staff_member_required, name='dispatch')
class MissingMediaView(TemplateView):

    def get(self, request):
        users = Tracker.objects.filter(
            event="media_missing").values('user').distinct()

        user_data = []
        for user in users:
            ud = {}
            ud['user'] = User.objects.get(pk=user['user'])
            missing_files = set()
            missing_for_user = Tracker.objects.filter(
                event="media_missing", user=ud['user'])
            for mfu in missing_for_user:
                data_json = json.loads(mfu.data)
                missing_files.add(data_json['filename'])
            ud['filenames'] = missing_files
            user_data.append(ud)

        return render(request, 'reports/missing_media.html',
                      {'user_data': user_data})


@method_decorator(staff_member_required, name='dispatch')
class MissingMediaPurgeView(TemplateView):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)

        return render(request, 'reports/missing_media_confirm_purge.html',
                      {'user': user})

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        Tracker.objects.filter(event="media_missing", user=user).delete()

        return render(request, 'reports/missing_media_purged.html',
                      {'user': user})
