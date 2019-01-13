# This is a workaround since Tastypie doesn't accept file Uploads
import math
import api

import os
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from oppia.models import Tag, CourseTag
from settings import constants
from settings.models import SettingProperties
from oppia.uploader import handle_uploaded_file


def add_course_tags(user, course, tags):
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
            ct = CourseTag.objects.get(course=course, tag=tag)
        except CourseTag.DoesNotExist:
            ct = CourseTag()
            ct.course = course
            ct.tag = tag
            ct.save()


def check_required_fields(request, validation_errors):
    required = ['username', 'password', 'tags', 'is_draft']

    for field in required:
        if field not in request.POST or request.POST[field].strip() == '':
            validation_errors.append("field '{0}' is missing or empty".format(field))
            
    if api.COURSE_FILE_FIELD not in request.FILES:
        validation_errors.append("Course file not found")
    else:
        course_file = request.FILES[api.COURSE_FILE_FIELD]
        if course_file is not None and course_file.content_type != 'application/zip' and course_file.content_type != 'application/x-zip-compressed':
             validation_errors.append("You may only upload a zip file")
             
    return validation_errors

def check_upload_file_size_type(file, validation_errors):
    max_upload = SettingProperties.get_int(constants.MAX_UPLOAD_SIZE, settings.OPPIA_MAX_UPLOAD_SIZE)
    if file is not None and file._size > max_upload:
        size = int(math.floor(max_upload / 1024 / 1024))
        validation_errors.append((_(u"Your file is larger than the maximum allowed (%(size)d Mb). You may want to check your course for large includes, such as images etc.") % {'size': size, }))

    if file is not None and file.content_type != 'application/zip' and file.content_type != 'application/x-zip-compressed':
        validation_errors.append(_(u"You may only upload a zip file"))

    return validation_errors


def authenticate_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        messages.error(request, _(u"Invalid username/password"))
        response_data = {
            'message': _('Authentication errors'),
            'messages': get_messages_array(request)
        }
        return False, response_data, None
    else:
        return True, None, user


@csrf_exempt
def publish_view(request):

    # get the messages to clear possible previous unprocessed messages
    get_messages_array(request)

    if request.method != 'POST':
        return HttpResponse(status=405)

    validation_errors = []
    validation_errors = check_required_fields(request, validation_errors)
    validation_errors = check_upload_file_size_type(request.FILES[api.COURSE_FILE_FIELD], validation_errors)

    if validation_errors:
        return JsonResponse({'errors': validation_errors}, status=400, )

    # authenticate user
    authenticated, response_data, user = authenticate_user(request, request.POST['username'], request.POST['password'])
    if not authenticated:
        return JsonResponse(response_data, status=401)

    # check user has permissions to publish course
    if settings.OPPIA_STAFF_ONLY_UPLOAD is True \
            and not user.is_staff \
            and user.userprofile.can_upload is False:
        return HttpResponse(status=401)

    extract_path = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', str(user.id))
    course, status_code = handle_uploaded_file(request.FILES[api.COURSE_FILE_FIELD], extract_path, request, user)
    
    if course is False:
        status = status_code if status_code is not None else 500
        response_data = {
            'messages': get_messages_array(request)
        }
        return JsonResponse(response_data, status=status)

    else:
        course.is_draft = (request.POST['is_draft'] == "True" or request.POST['is_draft'] == "true")
        course.save()

        # remove any existing tags
        CourseTag.objects.filter(course=course).delete()

        # add tags
        tags = request.POST['tags'].strip().split(",")
        add_course_tags(user, course, tags)

        msgs = get_messages_array(request)
        if len(msgs) > 0:
            return JsonResponse({'messages': msgs}, status=201)
        else:
            return HttpResponse(status=201)


def get_messages_array(request):
    msgs = messages.get_messages(request)
    response = []
    for msg in msgs:
        response.append({'tags': msg.tags, 'message': msg.message})
    return response
