# This is a workaround since Tastypie doesn't accept file Uploads
import math

import os
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from oppia.models import Tag, CourseTag
from oppia.settings import constants
from oppia.settings.models import SettingProperties
from oppia.uploader import handle_uploaded_file

COURSE_FILE_FIELD = 'course_file'

@csrf_exempt
def publish_view(request):

    # get the messages to clear possible previous unprocessed messages
    get_messages_array(request)

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
        max_upload = SettingProperties.get_int(constants.MAX_UPLOAD_SIZE, settings.OPPIA_MAX_UPLOAD_SIZE)
        if file is not None and file._size > max_upload:
            size = int(math.floor(max_upload / 1024 / 1024))
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
        messages.error(request, "Invalid username/password")
        response_data = {
            'message': _('Authentication errors'),
            'messages': get_messages_array(request)
        }
        return JsonResponse(response_data, status=401)
     
    # check user has permissions to publish course
    if settings.OPPIA_STAFF_ONLY_UPLOAD is True \
            and not user.is_staff \
            and user.userprofile.can_upload is False:
        return HttpResponse(status=401)
            
    extract_path = os.path.join(settings.COURSE_UPLOAD_DIR,'temp',str(user.id))
    course, response = handle_uploaded_file(request.FILES['course_file'], extract_path, request, user)

    if course is False:
        resp_code = response if response is not None else 500
        response_data = {
            'messages': get_messages_array(request)
        }
        return JsonResponse(response_data, status=resp_code)

    else:
        course.is_draft = (request.POST['is_draft'] == "True" or request.POST['is_draft'] == "true")
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

        msgs = get_messages_array(request)
        if len(msgs) > 0:
            return JsonResponse({'messages': msgs}, status=201)
        else:
            return HttpResponse(status=201)


def validate_fields(request):
    required = ['username','password','tags','is_draft']
    is_valid = True

    for r in required:
        if r not in request.POST:
            print r + " not found"
            messages.error(request, _("required field '%s' not found") % r)
            is_valid = False

    if 'course_file' not in request.FILES:
        print "Course file not found"
        messages.error(request, _("Course file not found"))
        is_valid = False
    else:
        course_file = request.FILES['course_file']
        if course_file is not None and course_file.content_type != 'application/zip' and course_file.content_type != 'application/x-zip-compressed':
            messages.error(request, _("You may only upload a zip file"))
            is_valid = False

    return is_valid

def get_messages_array(request):
    msgs = messages.get_messages(request)
    response = []
    for msg in msgs:
        response.append({'tags': msg.tags, 'message': msg.message })
    return response