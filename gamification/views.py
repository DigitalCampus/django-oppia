
import json
import os
import shutil
import zipfile
import xml.dom.minidom

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from gamification.forms import EditPointsForm
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

@staff_member_required
def edit_points(request, course_id):
    course = Course.objects.get(id=course_id)
    course_zip_file = os.path.join(settings.COURSE_UPLOAD_DIR, course.filename)
    zip = zipfile.ZipFile(course_zip_file,'r')
    xml_content = zip.read(course.shortname + "/module.xml")
    zip.close()
    # load existing course level points from the XML
    doc = xml.dom.minidom.parseString(xml_content)
    current_points = load_course_points(doc)
    #TODO if no course points then set to the defaults
    
    
    if request.method == 'POST':
        form = EditPointsForm(request.POST, initial = current_points)
        if form.is_valid():
            save_course_points(request, form, course)
    else:
        form = EditPointsForm(initial = current_points)

    return render(request, 'oppia/gamification/edit-points.html',
                              {'course': course,
                                  'form': form })
    
def load_course_points(doc):
    course_points = []
    try:
        for meta in doc.getElementsByTagName("meta")[:1]:
            for event in meta.getElementsByTagName("gamification")[:1][0].getElementsByTagName("event"):
                event_points = {}
                event_points['event'] = event.getAttribute("name")
                event_points['points'] = event.firstChild.nodeValue
                course_points.append(event_points)
                print(event_points)
    except IndexError: #xml does not have the gamification/events tag/s
        pass
    return course_points

def save_course_points(request, form, course):
    course_zip_file = os.path.join(settings.COURSE_UPLOAD_DIR, course.filename)
    zip = zipfile.ZipFile(course_zip_file,'a')
    xml_content = zip.read(course.shortname + "/module.xml")
    zip.close()
    doc = xml.dom.minidom.parseString(xml_content)
    for x in form.cleaned_data:
        print(x)
        print(form.cleaned_data[x])
        try:
            for meta in doc.getElementsByTagName("meta")[:1]:
                for event in meta.getElementsByTagName("gamification")[:1][0].getElementsByTagName("event"):
                    if event.getAttribute("name") == x:
                        event.firstChild.nodeValue = form.cleaned_data[x]
        except IndexError: #xml does not have the gamification/events tag/s
            pass
    
    temp_zip_path = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', str(request.user.id))
    module_xml = course.shortname + '/module.xml'
    try:
        os.makedirs(temp_zip_path)
    except OSError:
        pass # leaf dir for user already exists
    
    remove_from_zip(course_zip_file, temp_zip_path, course.shortname, module_xml)
    
    with zipfile.ZipFile(course_zip_file, 'a') as z:
        z.writestr(module_xml, doc.toprettyxml())
            
def remove_from_zip(zipfname, temp_zip_path, course_shortname, *filenames):
    try:
        tempname = os.path.join(temp_zip_path, course_shortname +'.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        print(item.filename)
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.copy(tempname, zipfname)
    finally:
        shutil.rmtree(temp_zip_path)

