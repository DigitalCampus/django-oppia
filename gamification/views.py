
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
    doc = get_module_xml(course, 'r')
    current_points = load_course_points(request, doc, course)  
    
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
    
def load_course_points(request, doc, course):
    course_custom_points = CourseGamificationEvent.objects.filter(course=course)
    if len(course_custom_points) > 0:
        return course_custom_points
    else:
        course_default_points = DefaultGamificationEvent.objects.exclude(level=DefaultGamificationEvent.GLOBAL)
        initialise_course_points(request, course, course_default_points)
        return course_default_points

def save_course_points(request, form, course):
    
    doc = get_module_xml(course, 'a')
    
    gamification_node = get_course_gamification_node(doc)
    
    if gamification_node:
        for x in form.cleaned_data:
            for event in gamification_node.getElementsByTagName("event"):
                if event.getAttribute("name") == x:
                    event.firstChild.nodeValue = form.cleaned_data[x]
    else:
        meta = doc.getElementsByTagName("meta")[:1][0]
        gamification = doc.createElement("gamification")
        for x in form.cleaned_data:
            event = doc.createElement("event")
            event.setAttribute("name", x)
            value = doc.createTextNode(str(form.cleaned_data[x]))
            event.appendChild(value)
            gamification.appendChild(event)
        meta.appendChild(gamification)
    
    # update the gamification tables
    CourseGamificationEvent.objects.filter(course=course).delete()
    for x in form.cleaned_data:
        course_game_event = CourseGamificationEvent()
        course_game_event.user = request.user
        course_game_event.course = course
        course_game_event.event = x
        course_game_event.points = form.cleaned_data[x]
        course_game_event.save()
    
    rewrite_zip_file(request, course, doc)
    update_course_version_no(request, course)

def save_activity_points(request, form, course, activity):
    
    doc = get_module_xml(course, 'a')
    
    add_gamification_node = False

    activity_nodes = doc.getElementsByTagName("activity")
    update_node = None
    
    for activity_node in activity_nodes:
        if activity_node.getAttribute("digest") == activity.digest:
            update_node = activity_node            
    if update_node == None:
        return
    
    try:
        for x in form.cleaned_data:
            for event in update_node.getElementsByTagName("gamification")[:1][0].getElementsByTagName("event"):
                if event.getAttribute("name") == x:
                    event.firstChild.nodeValue = form.cleaned_data[x]
    except IndexError: #xml does not have the gamification/events tag/s
        add_gamification_node = True

    if add_gamification_node:
        gamification = doc.createElement("gamification")
        for x in form.cleaned_data:
            event = doc.createElement("event")
            event.setAttribute("name", x)
            value = doc.createTextNode(str(form.cleaned_data[x]))
            event.appendChild(value)
            gamification.appendChild(event)
        update_node.appendChild(gamification)
    
    # update the gamification tables
    ActivityGamificationEvent.objects.filter(activity=activity).delete()
    for x in form.cleaned_data:
        activity_game_event = ActivityGamificationEvent()
        activity_game_event.user = request.user
        activity_game_event.activity = activity
        activity_game_event.event = x
        activity_game_event.points = form.cleaned_data[x]
        activity_game_event.save()
            
    rewrite_zip_file(request, course, doc)
    update_course_version_no(request, course)


def save_media_points(request, form, course, media):
    
    doc = get_module_xml(course, 'a')
    
    add_gamification_node = False

    media_element_list = [node for node in doc.firstChild.childNodes if node.nodeName == 'media']
    media_element = None
    if len(media_element_list) > 0:
        media_element = media_element_list[0]

    update_node = None
    
    for file_node in media_element.childNodes:
        if file_node.nodeName == 'file' and file_node.getAttribute("digest") == media.digest:
            update_node = file_node            
    if update_node == None:
        return
    
    try:
        for x in form.cleaned_data:
            for event in update_node.getElementsByTagName("gamification")[:1][0].getElementsByTagName("event"):
                if event.getAttribute("name") == x:
                    event.firstChild.nodeValue = form.cleaned_data[x]
    except IndexError: #xml does not have the gamification/events tag/s
        add_gamification_node = True

    if add_gamification_node:
        gamification = doc.createElement("gamification")
        for x in form.cleaned_data:
            event = doc.createElement("event")
            event.setAttribute("name", x)
            value = doc.createTextNode(str(form.cleaned_data[x]))
            event.appendChild(value)
            gamification.appendChild(event)
        update_node.appendChild(gamification)
    
    # update the gamification tables
    MediaGamificationEvent.objects.filter(media=media).delete()
    for x in form.cleaned_data:
        media_game_event = MediaGamificationEvent()
        media_game_event.user = request.user
        media_game_event.media = media
        media_game_event.event = x
        media_game_event.points = form.cleaned_data[x]
        media_game_event.save()
            
    rewrite_zip_file(request, course, doc)
    update_course_version_no(request, course)



def get_module_xml(course, mode): 
    course_zip_file = os.path.join(settings.COURSE_UPLOAD_DIR, course.filename)
    zip = zipfile.ZipFile(course_zip_file, mode)
    xml_content = zip.read(course.shortname + "/module.xml")
    zip.close()
    doc = xml.dom.minidom.parseString(xml_content)
    return doc

def get_course_gamification_node(doc):
    meta = doc.getElementsByTagName("meta")[:1][0]
    for node in meta.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.tagName == 'gamification':
            return node
    return None

def findChildNodeByName(parent, name):
    for node in parent.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.localName == name:
            return node
    return None
  
def update_course_version_no(request, course):
    new_version_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #update db
    course.version = new_version_id
    course.lastupdated_date = timezone.now()
    course.save()
    
    #update module.xml
    doc = get_module_xml(course, 'a')
    meta = doc.getElementsByTagName("meta")[:1][0]
    version_id = meta.getElementsByTagName("versionid")[0]
    version_id.firstChild.nodeValue = new_version_id
    rewrite_zip_file(request, course, doc)

def rewrite_zip_file(request, course, doc):
    temp_zip_path = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', str(request.user.id))
    module_xml = course.shortname + '/module.xml'
    try:
        os.makedirs(temp_zip_path)
    except OSError:
        pass # leaf dir for user id already exists
    
    course_zip_file = os.path.join(settings.COURSE_UPLOAD_DIR, course.filename)
    remove_from_zip(course_zip_file, temp_zip_path, course.shortname, module_xml)

    xml_content = doc.toprettyxml(indent='',newl='', encoding='utf-8')

    with zipfile.ZipFile(course_zip_file, 'a') as z:
        z.writestr(module_xml, xml_content)

def remove_from_zip(zipfname, temp_zip_path, course_shortname, *filenames):
    try:
        tempname = os.path.join(temp_zip_path, course_shortname +'.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.copy(tempname, zipfname)
    finally:
        shutil.rmtree(temp_zip_path)

def initialise_course_points(request, course, course_points):
    CourseGamificationEvent.objects.filter(course=course).delete()
    for event in course_points:
        course_game_event = CourseGamificationEvent()
        course_game_event.user = request.user
        course_game_event.course = course
        course_game_event.event = event.event
        course_game_event.points = event.points
        course_game_event.save()
