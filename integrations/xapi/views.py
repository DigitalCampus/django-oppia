# integrations/xapi/views.py
import datetime
import json
import tablib

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from oppia.models import Tracker, Activity
from quiz.models import QuizAttempt
from json.decoder import JSONDecodeError


@method_decorator(staff_member_required, name='dispatch')
class HomeView(TemplateView):

    def get(self, request):
        return render(request, 'integrations/xapi/index.html')


@method_decorator(staff_member_required, name='dispatch')
class CSVExportView(TemplateView):

    def get(self, request):

        start_date = timezone.now() - datetime.timedelta(days=7)
        end_date = timezone.now()

        headers = ('user_id',
                   'course_id',
                   'course_title',
                   'attempt_date',
                   'submitted_date',
                   'type',
                   'quiz_id',
                   'quiz_title',
                   'section_title',
                   'completed',
                   'time_taken',
                   'score',
                   'maxscore')

        data = []
        data = tablib.Dataset(*data, headers=headers)

        trackers = Tracker.objects.filter(submitted_date__gte=start_date,
                                          submitted_date__lte=end_date,
                                          type=Activity.QUIZ)

        for tracker in trackers:
            # Get the matching quiz attempt object
            try:
                tracker_data = json.loads(tracker.data)
                quiz_instance = tracker_data['instance_id']
            except JSONDecodeError:
                continue

            try:
                quiz_attempt = QuizAttempt.objects.get(
                    instance_id=quiz_instance)
            except QuizAttempt.DoesNotExist:
                continue

            data.append(
                        (
                           tracker.user.id,
                           tracker.course.id,
                           tracker.course.title,
                           quiz_attempt.attempt_date,
                           tracker.submitted_date,
                           tracker.type,
                           quiz_attempt.quiz.id,
                           quiz_attempt.quiz.title,
                           tracker.section_title,
                           tracker.completed,
                           tracker.time_taken,
                           quiz_attempt.score,
                           quiz_attempt.maxscore
                        )
                    )

        response = HttpResponse(data.csv,
                                content_type='application/text;charset=utf-8')
        response['Content-Disposition'] = \
            "attachment; filename=xapi-export.csv"

        return response
