# oppia/permissions.py

from django.conf import settings
from oppia.models import Course

def can_upload(request):
    if settings.OPPIA_STAFF_ONLY_UPLOAD is True and not request.user.is_staff and request.user.userprofile.can_upload is False:
        return False
    else:
        return True
           
def check_owner(request,id):
    try:
        # check only the owner can view 
        if request.user.is_staff:
            course = Course.objects.get(pk=id)
        else:
            try:
                course = Course.objects.get(pk=id,user=request.user)
            except Course.DoesNotExist:
                course = Course.objects.get(pk=id,coursemanager__course__id=id, coursemanager__user = request.user)
    except Course.DoesNotExist:
        raise Http404
    return course

def is_manager(course_id,user):
    try:
        # check only the owner can view 
        if user.is_staff:
            return True
        else:
            try:
                course = Course.objects.get(pk=course_id,user=user)
                return True
            except Course.DoesNotExist:
                course = Course.objects.get(pk=course_id,coursemanager__course__id=course_id, coursemanager__user = user)
                return True
    except Course.DoesNotExist:
        return False


def course_can_view(request,id):
    try:
        if request.user.is_staff:
            course = Course.objects.get(pk=id)
        else:
            try:
                course = Course.objects.get(pk=id,is_draft=False,is_archived=False)
            except Course.DoesNotExist:
                course = Course.objects.get(pk=id,is_draft=False,is_archived=False, coursemanager__course__id=id, coursemanager__user = request.user)
    except Course.DoesNotExist:
        raise Http404
    return course