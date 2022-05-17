
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from gamification.forms import GamificationEventForm
from gamification.models import DefaultGamificationEvent, \
                                CourseGamificationEvent, \
                                ActivityGamificationEvent, \
                                MediaGamificationEvent
from gamification.xml_writer import GamificationXMLWriter
from oppia.models import Course, Points, Activity, Media
from oppia.permissions import can_edit_course, can_edit_course_gamification


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


def edit_course_gamification(request, course_id):
    if not can_edit_course_gamification(request, course_id):
        raise PermissionDenied

    course = get_object_or_404(Course, pk=course_id)

    events_formset = formset_factory(GamificationEventForm,
                                     extra=0,
                                     can_delete=True)
    if request.method == 'POST':
        formset = events_formset(request.POST, request.FILES, prefix='events')
        process_edit_gamification_post(request, course, events_formset)
    else:
        formset = events_formset(prefix='events')

    activities = Activity.objects.filter(section__course=course) \
        .select_related('section') \
        .prefetch_related('gamification_events')
    media = Media.objects.filter(course=course) \
        .prefetch_related('gamification_events')

    default_points = {
        'course': DefaultGamificationEvent.objects
        .exclude(level=DefaultGamificationEvent.GLOBAL),
        'activity': DefaultGamificationEvent.objects
        .filter(level=DefaultGamificationEvent.ACTIVITY),
        'quiz': DefaultGamificationEvent.objects
        .filter(level=DefaultGamificationEvent.QUIZ),
        'media': DefaultGamificationEvent.objects
        .filter(level=DefaultGamificationEvent.MEDIA)
    }

    course_events = CourseGamificationEvent.objects.filter(course=course)
    course.events = {}
    for event in course_events:
        course.events[event.event] = event.points

    for activity in activities:
        activity.events = {}
        for event in activity.gamification_events.all():
            activity.events[event.event] = event.points

    for m in media:
        m.events = {}
        for event in m.gamification_events.all():
            m.events[event.event] = event.points

    return render(request, 'gamification/edit.html',
                  {'default_points': default_points,
                   'course': course,
                   'events_formset': formset,
                   'course_events': course_events,
                   'activities': activities,
                   'media': media})


def process_edit_gamification_post(request, course, events_formset):
    formset = events_formset(request.POST, request.FILES, prefix='events')
    if formset.is_valid():

        updated = False
        for form in formset:
            process_gamification_formset(request, formset, form)
            updated = True

        if updated:
            writer = GamificationXMLWriter(course)
            new_version = writer.update_gamification(request.user)
            messages.success(request,
                             'Course XML updated. New version: {}'
                             .format(new_version))


def process_gamification_formset(request, formset, form):
    # extract name from each form and save
    event = form.cleaned_data.get('event')
    level = form.cleaned_data.get('level')
    points = form.cleaned_data.get('points')
    reference = form.cleaned_data.get('reference')
    defaults = {'points': points, 'user': request.user}

    to_delete = formset.can_delete \
        and formset._should_delete_form(form)

    if level == 'course':
        if to_delete:
            CourseGamificationEvent.objects \
                .filter(course_id=reference,
                        event=event).delete()
        else:
            CourseGamificationEvent.objects \
                .update_or_create(course_id=reference,
                                  event=event,
                                  defaults=defaults)
    elif level == 'activity':
        if to_delete:
            ActivityGamificationEvent.objects \
                .filter(activity_id=reference,
                        event=event).delete()
        else:
            ActivityGamificationEvent.objects \
                .update_or_create(activity_id=reference,
                                  event=event,
                                  defaults=defaults)
    elif level == 'media':
        if to_delete:
            MediaGamificationEvent.objects \
                .filter(media_id=reference,
                        event=event).delete()
        else:
            MediaGamificationEvent.objects \
                .update_or_create(media_id=reference,
                                  event=event,
                                  defaults=defaults)
