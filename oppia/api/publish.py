# This is a workaround since Tastypie doesn't accept file Uploads
import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from oppia.uploader import handle_uploaded_file
from oppia.models import Tag, CourseTag
from django.contrib import messages

@csrf_exempt
def publish_view(request):
    
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    required = ['username','password','tags','is_draft']
   
    for r in required:
        if r not in request.POST:
            print r + " not found"
            return HttpResponse(status=400)
   
    
    if 'course_file' not in request.FILES:
        print "Course file not found"
        return HttpResponse(status=400)
        
    # authenticate user
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return HttpResponse(status=401)
     
    # check user has permissions to publish course
    if settings.OPPIA_STAFF_ONLY_UPLOAD is True and not user.is_staff and user.userprofile.can_upload is False:
        return HttpResponse(status=401)
            
    extract_path = os.path.join(settings.COURSE_UPLOAD_DIR,'temp',str(user.id))
    course = handle_uploaded_file(request.FILES['course_file'], extract_path, request, user)

    if course is False:
        return HttpResponse(status=500)
    else:
        if request.POST['is_draft'] == "False":
            course.is_draft = False
        else:
            course.is_draft = True
        course.save()
        
        # remove any existing tags
        CourseTag.objects.filter(course=course).delete()
        
        # add tags
        tags = request.POST['tags'].strip().split(",")
        for t in tags:
            try: 
                tag = Tag.objects.get(name__iexact=t.strip())
            except Tag.DoesNotExist:
                tag = Tag()
                tag.name = t.strip()
                tag.created_by = user
                tag.save()
            # add tag to course
            try:
                ct = CourseTag.objects.get(course=course,tag=tag)
            except CourseTag.DoesNotExist:
                ct = CourseTag()
                ct.course = course
                ct.tag = tag
                ct.save()
        
        return HttpResponse(status=201)
    