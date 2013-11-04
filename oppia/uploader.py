# oppia/uploader.py
import datetime
import json
import os
import xml.dom.minidom
import zipfile
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from oppia.models import Course, Section, Activity, Media
from xml.dom.minidom import Node

def handle_uploaded_file(f, extract_path, request):
    zipfilepath = settings.COURSE_UPLOAD_DIR + f.name
    
    with open(zipfilepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
    zip = zipfile.ZipFile(zipfilepath)
    zip.extractall(path=extract_path)      
    
    mod_name = ''
    for dir in os.listdir(extract_path)[:1]:
        mod_name = dir
       
    # check there is at least a sub dir 
    if mod_name == '':
        messages.info(request,_("Invalid course zip file"))
        return False
    
    # check that the 
    if not os.path.isfile(extract_path + mod_name + "/module.xml"):
        messages.info(request,_("Zip file does not contain a module.xml file"))
        return False
      
    # parse the module.xml file
    doc = xml.dom.minidom.parse(extract_path + mod_name + "/module.xml") 
    for meta in doc.getElementsByTagName("meta")[:1]:
        versionid = 0
        for v in meta.getElementsByTagName("versionid")[:1]:
            versionid = int(v.firstChild.nodeValue)
        temp_title = {}
        for t in meta.childNodes:
            if t.nodeName == "title":
                temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
        title = json.dumps(temp_title)
        shortname = ''
        for sn in meta.getElementsByTagName("shortname")[:1]:
            shortname = sn.firstChild.nodeValue
    
    old_course_filename = None
    # Find if course already exists
    try: 
        course = Course.objects.get(shortname = shortname)
        old_course_filename = course.filename
         
        # check that the current user is allowed to wipe out the other course
        if course.user != request.user:
            messages.info(request,_("Sorry, only the original owner may update this course"))
            return False
        
        # check if course version is older
        if course.version > versionid:
            messages.info(request,_("A newer version of this course already exists"))
            return False
        # wipe out the old sections/activities/media
        oldsections = Section.objects.filter(course = course)
        oldsections.delete()
        oldmedia = Media.objects.filter(course = course)
        oldmedia.delete()
        
        course.shortname = shortname
        course.title = title
        course.version = versionid
        course.user = request.user
        course.filename = f.name
        course.lastupdated_date = datetime.datetime.now()
        course.save()
    except Course.DoesNotExist:
        course = Course()
        course.shortname = shortname
        course.title = title
        course.version = versionid
        course.user = request.user
        course.filename = f.name
        course.save()
    
    
            
    # add in any baseline activities
    for meta in doc.getElementsByTagName("meta")[:1]:
        if meta.getElementsByTagName("activity").length > 0:
            section = Section()
            section.course = course
            section.title = '{"en": "Baseline"}'
            section.order = 0
            section.save()
            for a in meta.getElementsByTagName("activity"):
                temp_title = {}
                for t in a.getElementsByTagName("title"):
                    temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
                title = json.dumps(temp_title)
                activity = Activity()
                activity.section = section
                activity.order = a.getAttribute("order")
                activity.title = title
                activity.type = a.getAttribute("type")
                activity.digest = a.getAttribute("digest")
                activity.baseline = True
                activity.save()
            
       
    # add all the sections
    for structure in doc.getElementsByTagName("structure")[:1]:
        
        if structure.getElementsByTagName("section").length == 0:
            messages.info(request,_("There don't appear to be any activities in this upload file."))
            course.delete()
            return False
        
        for s in structure.getElementsByTagName("section"):
            temp_title = {}
            for t in s.childNodes:
                if t.nodeName == 'title':
                    temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
            title = json.dumps(temp_title)
            section = Section()
            section.course = course
            section.title = title
            section.order = s.getAttribute("order")
            section.save()
            
            # add all the activities
            for activities in s.getElementsByTagName("activities")[:1]:
                for a in activities.getElementsByTagName("activity"):
                    temp_title = {}
                    for t in a.getElementsByTagName("title"):
                        temp_title[t.getAttribute('lang')] = t.firstChild.nodeValue
                    title = json.dumps(temp_title)
                    activity = Activity()
                    activity.section = section
                    activity.order = a.getAttribute("order")
                    activity.title = title
                    activity.type = a.getAttribute("type")
                    activity.digest = a.getAttribute("digest")
                    activity.baseline = False
                    activity.save()
                    
    # add all the media
    for files in doc.lastChild.lastChild.childNodes:
        if files.nodeName == 'file':
            media = Media()
            media.course = course
            media.filename = files.getAttribute("filename")
            media.download_url = files.getAttribute("download_url")
            media.digest = files.getAttribute("digest")
            media.save()
    
    if old_course_filename is not None and course.version != versionid:
        os.remove(settings.COURSE_UPLOAD_DIR + old_course_filename)
    return course       
              