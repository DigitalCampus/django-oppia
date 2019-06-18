
import datetime
import json
import os
import shutil
import zipfile
import xml.dom.minidom

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from gamification.forms import EditCoursePointsForm, EditActivityPointsForm, EditMediaPointsForm
from gamification.models import *
from gamification.xml_writer import GamificationXMLWriter
from oppia.models import Points, Course, Section, Activity
from oppia.permissions import *

from pydoc import doc
from platform import node


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


def edit_course_points(request, course_id):
    if not can_edit_course(request, course_id):
        raise exceptions.PermissionDenied
    
    course = get_object_or_404(Course, pk=course_id)
    current_points = load_course_points(request, course)
    
    if request.method == 'POST':
        form = EditCoursePointsForm(request.POST, initial = current_points)
        if form.is_valid():
            save_course_points(request, form, course)
            
            return HttpResponseRedirect(reverse('oppia_gamification_course_points_updated', args=[course.id]))  # Redirect after POST
    else:
        form = EditCoursePointsForm(initial = current_points)

    return render(request, 'oppia/gamification/edit-course-points.html',
                              {'course': course,
                                  'form': form })

def course_points_updated(request, course_id):
    if not can_edit_course(request, course_id):
        raise exceptions.PermissionDenied
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'oppia/gamification/course-points-updated.html',
                              {'course': course })


def view_activity_points(request, course_id):
    if not can_edit_course(request, course_id):
        raise exceptions.PermissionDenied
    
    course = get_object_or_404(Course, pk=course_id)
    sections = Section.objects.filter(course=course).order_by('order')
    
    return render(request, 'oppia/gamification/view-activity-points.html',
                              {'course': course,
                               'sections': sections })


def edit_activity_points(request, course_id, activity_id):
    if not can_edit_course(request, course_id):
        raise exceptions.PermissionDenied
    
    course = get_object_or_404(Course, pk=course_id)
    activity = get_object_or_404(Activity, pk=activity_id, section__course=course)
    
    if request.method == 'POST':
        form = EditActivityPointsForm(request.POST, initial = activity.get_event_points()['events'])
        if form.is_valid():
            save_activity_points(request, form, course, activity)
            return HttpResponseRedirect(reverse('oppia_gamification_view_activity_points', args=[course_id]))  # Redirect after POST
    else:
        form = EditActivityPointsForm(initial = activity.get_event_points()['events'])
    
    return render(request, 'oppia/gamification/edit-activity-points.html',
                              {'course': course,
                               'activity': activity,
                               'form': form })
 
 
def view_media_points(request, course_id):
    if not can_edit_course(request, course_id):
        raise exceptions.PermissionDenied
    
    course = get_object_or_404(Course, pk=course_id)
    media = Media.objects.filter(course=course)
    
    return render(request, 'oppia/gamification/view-media-points.html',
                              {'course': course,
                               'media': media }) 

def edit_media_points(request, course_id, media_id):
    if not can_edit_course(request, course_id):
        raise exceptions.PermissionDenied
    
    course = get_object_or_404(Course, pk=course_id)
    media = get_object_or_404(Media, pk=media_id)
    
    if request.method == 'POST':
        form = EditMediaPointsForm(request.POST, initial = media.get_event_points()['events'])
        if form.is_valid():
            save_media_points(request, form, course, media)
            return HttpResponseRedirect(reverse('oppia_gamification_view_media_points', args=[course_id]))  # Redirect after POST
    else:
        form = EditMediaPointsForm(initial = media.get_event_points()['events'])
    
    return render(request, 'oppia/gamification/edit-media-points.html',
                              {'course': course,
                               'media': media,
                               'form': form })


def load_course_points(request, course):
    course_custom_points = CourseGamificationEvent.objects.filter(course=course)
    if len(course_custom_points) > 0:
        return course_custom_points
    else:
        course_default_points = DefaultGamificationEvent.objects.exclude(level=DefaultGamificationEvent.GLOBAL)
        initialise_course_points(request, course, course_default_points)
        return course_default_points


def initialise_course_points(request, course, course_points):
    CourseGamificationEvent.objects.filter(course=course).delete()
    for event in course_points:
        course_game_event = CourseGamificationEvent()
        course_game_event.user = request.user
        course_game_event.course = course
        course_game_event.event = event.event
        course_game_event.points = event.points
        course_game_event.save()


def save_course_points(request, form, course):
    # update the gamification tables
    CourseGamificationEvent.objects.filter(course=course).delete()
    for x in form.cleaned_data:
        course_game_event = CourseGamificationEvent()
        course_game_event.user = request.user
        course_game_event.course = course
        course_game_event.event = x
        course_game_event.points = form.cleaned_data[x]
        course_game_event.save()

    writer = GamificationXMLWriter(course)
    new_version = writer.update_gamification(request.user)


def save_activity_points(request, form, course, activity):
    # update the gamification tables
    ActivityGamificationEvent.objects.filter(activity=activity).delete()
    for x in form.cleaned_data:
        activity_game_event = ActivityGamificationEvent()
        activity_game_event.user = request.user
        activity_game_event.activity = activity
        activity_game_event.event = x
        activity_game_event.points = form.cleaned_data[x]
        activity_game_event.save()

    writer = GamificationXMLWriter(course)
    new_version = writer.update_gamification(request.user)


def save_media_points(request, form, course, media):
    MediaGamificationEvent.objects.filter(media=media).delete()
    for x in form.cleaned_data:
        media_game_event = MediaGamificationEvent()
        media_game_event.user = request.user
        media_game_event.media = media
        media_game_event.event = x
        media_game_event.points = form.cleaned_data[x]
        media_game_event.save()

    writer = GamificationXMLWriter(course)
    new_version = writer.update_gamification(request.user)


def edit_course_gamification(request, course_id):
    if not can_edit_course(request, course_id):
        raise exceptions.PermissionDenied

    course = get_object_or_404(Course, pk=course_id)
    activities = Activity.objects.filter(section__course=course).prefetch_related('gamification_events')
    media = Media.objects.filter(course=course)

    default_points = {
        'course': DefaultGamificationEvent.objects.exclude(level=DefaultGamificationEvent.GLOBAL),
        'activity': DefaultGamificationEvent.objects.filter(level=DefaultGamificationEvent.ACTIVITY),
        'quiz': DefaultGamificationEvent.objects.filter(level=DefaultGamificationEvent.QUIZ),
        'media': DefaultGamificationEvent.objects.filter(level=DefaultGamificationEvent.MEDIA),
    }

    course_events = CourseGamificationEvent.objects.filter(course=course)
    course.events = {}
    for event in course_events:
        course.events[event.event] = event.points


    for activity in activities:
        activity.events = {}
        for event in activity.gamification_events.all():
            activity.events[event.event] = event.points



    return render(request, 'oppia/gamification/edit.html',
                  {
                    'default_points':default_points,
                  'course': course,
                   'course_events': course_events,
                   'activities':activities,
                   'media': media})


