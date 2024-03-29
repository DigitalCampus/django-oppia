
import warnings

from django.urls import reverse
from tastypie.models import ApiKey

from oppia.models import Course


warnings.warn("get_api_key function will be removed in v0.16.0", DeprecationWarning, stacklevel=2)


def get_api_key(user):
    """
    Returns the ApiKey for a user object.
    If it does not exist yet, is generated
    """
    try:
        api_key = ApiKey.objects.get(user=user)
    except ApiKey.DoesNotExist:
        # if the user doesn't have an apiKey yet, generate it
        api_key = ApiKey.objects.create(user=user)
    return api_key


warnings.warn("get_api_url function will be removed in v0.16.0", DeprecationWarning, stacklevel=2)


def get_api_url(version, resource_name, resource_id=None):
    view_name = 'api_dispatch_list' \
        if resource_id is None else 'api_dispatch_detail'
    kwargs = {'resource_name': resource_name, 'api_name': version}
    if resource_id is not None:
        kwargs['pk'] = resource_id
    return reverse(view_name, kwargs=kwargs)


def update_course_status(id, course_status):
    course = Course.objects.get(pk=id)
    original_status = course.status
    course.status = course_status
    course.save()
    return original_status


def update_course_owner(id, owner_id):
    course = Course.objects.get(pk=id)
    course.user_id = owner_id
    course.save()


def get_file_contents(filename):
    with open(filename, 'r') as f:
        return f.read()
