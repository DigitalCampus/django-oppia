# This is a workaround since Tastypie doesn't accept file Uploads
import math

import os
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from oppia.models import Tag, CourseTag
from oppia.uploader import handle_uploaded_file

COURSE_FILE_FIELD = 'course_file'

@csrf_exempt
def publish_view(request):

    if request.method != 'POST':
        return HttpResponse(status=405)

    required = ['username','password','tags','is_draft']

    validationErrors = []

    for field in required:
        if field not in request.POST:
            print field + " not found"
            validationErrors.append("field '{0}' missing".format(field))


    if COURSE_FILE_FIELD not in request.FILES:
        print "Course file not found"
        validationErrors.append("file '{0}' missing".format(COURSE_FILE_FIELD))
    else:
        # check the file size of the course doesnt exceed the max
        file = request.FILES[COURSE_FILE_FIELD]
        if file is not None and file._size > settings.OPPIA_MAX_UPLOAD_SIZE:
            size = int(math.floor(settings.OPPIA_MAX_UPLOAD_SIZE / 1024 / 1024))
            validationErrors.append((_("Your file is larger than the maximum allowed (%(size)d Mb). You may want to check your course for large includes, such as images etc.") % {'size':size, }))

        if file is not None and file.content_type != 'application/zip' and file.content_type != 'application/x-zip-compressed':
            validationErrors.append(_("You may only upload a zip file"))

    if validationErrors:
        return JsonResponse({ 'errors' : validationErrors }, status=400, )
        
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
    