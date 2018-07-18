
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from oppia.models import Points, Course


@staff_member_required
def leaderboard_export(request, course_id=None):

    if request.is_secure():
        prefix = 'https://'
    else:
        prefix = 'http://'

    response_data = {}
    response_data['generated_date'] = timezone.now()
    response_data['server'] = prefix + request.META['SERVER_NAME']

    if course_id is None:
        leaderboard = Points.get_leaderboard()
    else:
        course = get_object_or_404(Course, pk=course_id)
        leaderboard = Points.get_leaderboard(course=course)
        response_data['course'] = course.shortname

    response_data['leaderboard'] = []

    for idx, leader in enumerate(leaderboard):
        leader_data = {}
        leader_data['position'] = idx + 1
        leader_data['username'] = leader.username
        leader_data['first_name'] = leader.first_name
        leader_data['last_name'] = leader.last_name
        leader_data['points'] = leader.total
        leader_data['badges'] = leader.badges
        response_data['leaderboard'].append(leader_data)

    return JsonResponse(response_data)
