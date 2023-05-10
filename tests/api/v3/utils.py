import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405

# @TODO complete fully with correct info


def get_admin_user():
    return User.objects.get(username="admin")


def get_staff_user():
    return User.objects.get(username="staff")


def get_teacher_user():
    return User.objects.get(username="teacher")


'''
for admin user
'''


def get_auth_header_admin():
    return {'AUTH': 'admin:admin_api_key'}


'''
for standard user
'''


def get_auth_header_user():
    return {'AUTH': 'demo:demo_api_key'}


'''
invalid auth credentials
'''


def get_auth_header_invalid():
    return {'AUTH': 'not_a_user:invalid_api_key'}


'''
for teacher user
'''


def get_auth_header_teacher():
    return {'AUTH': 'teacher:teacher_api_key'}


'''
for staff user
'''


def get_auth_header_staff():
    return {'AUTH': 'staff:staff_api_key'}


# Copy test courses to upload directory
def copy_test_courses(courses_to_copy):
    for test_course in courses_to_copy:
        src = os.path.join(settings.TEST_RESOURCES, test_course)
        dst = os.path.join(settings.COURSE_UPLOAD_DIR, test_course)
        shutil.copyfile(src, dst)
