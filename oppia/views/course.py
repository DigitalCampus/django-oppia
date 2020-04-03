import os

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from oppia.forms.upload import UploadCourseStep1Form, UploadCourseStep2Form
from oppia.models import Tag, \
                         CourseTag, \
                         CoursePublishingLog, \
                         Course
from oppia.permissions import can_edit_course, \
                              can_view_course, \
                              can_view_course_detail, \
                              user_can_upload, \
                              can_view_courses_list
from oppia.signals import course_downloaded
from oppia.uploader import handle_uploaded_file
from oppia.views.utils import get_paginated_courses
from reports.signals import dashboard_accessed
from summary.models import UserCourseSummary


def render_courses_list(request, courses, params=None):

    if params is None:
        params = {}

    course_filter = request.GET.get('visibility', '')
    if course_filter == 'draft':
        courses = courses.filter(is_draft=True)
    elif course_filter == 'archived':
        courses = courses.filter(is_archived=True)

    tag_list = Tag.objects.all().exclude(coursetag=None).order_by('name')
    paginator = Paginator(courses, 25)  # Show 25 per page
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET. get('page', '1'))
    except ValueError:
        page = 1

    course_stats = list(UserCourseSummary.objects.filter(course__in=courses)
                        .values('course')
                        .annotate(distinct=Count('user'),
                                  total=Sum('total_downloads')))

    try:
        courses = paginator.page(page)
    except (EmptyPage, InvalidPage):
        courses = paginator.page(paginator.num_pages)

    for course in courses:
        access_detail = can_view_course_detail(request, course.id)
        course.can_edit = can_edit_course(request, course.id)
        course.access_detail = access_detail is not None

        for stats in course_stats:
            if stats['course'] == course.id:
                course.distinct_downloads = stats['distinct']
                course.total_downloads = stats['total']
                # remove the element to optimize next searches
                course_stats.remove(stats)

    params['page'] = courses
    params['tag_list'] = tag_list
    params['course_filter'] = course_filter

    return render(request, 'course/list.html', params)


def tag_courses_view(request, tag_id):
    courses = can_view_courses_list(request)

    courses = courses.filter(coursetag__tag__pk=tag_id)

    dashboard_accessed.send(sender=None, request=request, data=None)
    return render_courses_list(request, courses, {'current_tag': tag_id})


def courses_list_view(request):

    if request.is_ajax():
        # if we are requesting via ajax, just show the course list
        ordering, courses = get_paginated_courses(request)
        return render(request, 'course/list_page.html',
                      {'page': courses,
                          'page_ordering': ordering,
                          'ajax_url': request.path})
    else:
        courses = can_view_courses_list(request)

        dashboard_accessed.send(sender=None, request=request, data=None)
        return render_courses_list(request, courses)


class CourseDownload(TemplateView):

    def get(self, request, course_id):
        course = can_view_course(request, course_id)
        file_to_download = course.getAbsPath()
        binary_file = open(file_to_download, 'rb')
        response = HttpResponse(binary_file.read(),
                                content_type='application/zip')
        binary_file.close()
        response['Content-Length'] = os.path.getsize(file_to_download)
        response['Content-Disposition'] = 'attachment; filename="%s"' \
            % (course.filename)

        course_downloaded.send(sender=self, course=course, request=request)

        return response


@user_can_upload
def upload_step1(request):
    if request.method == 'POST':
        form = UploadCourseStep1Form(request.POST, request.FILES)
        if form.is_valid():  # All validation rules pass
            extract_path = os.path.join(settings.COURSE_UPLOAD_DIR,
                                        'temp',
                                        str(request.user.id))
            course, resp = handle_uploaded_file(request.FILES['course_file'],
                                                extract_path,
                                                request,
                                                request.user)
            if course:
                CoursePublishingLog(course=course,
                                    user=request.user,
                                    action="file_uploaded",
                                    data=request.FILES['course_file'].name) \
                                .save()
                return HttpResponseRedirect(reverse('oppia:upload_step2',
                                                    args=[course.id]))
    else:
        form = UploadCourseStep1Form()  # An unbound form

    return render(request, 'course/form.html',
                  {'form': form,
                   'title': _(u'Upload Course - step 1')})


@user_can_upload
def upload_step2(request, course_id, editing=False):

    if (editing and not can_edit_course(request, course_id)):
        raise PermissionDenied

    course = Course.objects.get(pk=course_id)

    if request.method == 'POST':
        form = UploadCourseStep2Form(request.POST, request.FILES)
        if form.is_valid() and course:
            # add the tags

            update_course_tags(form, course, request.user)
            redirect = 'oppia:course' if editing else 'oppia:upload_success'
            CoursePublishingLog(
                course=course,
                new_version=course.version,
                user=request.user,
                action="upload_course_published",
                data=_(u'Course published via file upload')).save()
            return HttpResponseRedirect(reverse(redirect))
    else:
        form = UploadCourseStep2Form(initial={'tags': course.get_tags(),
                                              'is_draft': course.is_draft, })

    page_title = _(u'Upload Course - step 2') \
        if not editing else _(u'Edit course')
    return render(request, 'course/form.html',
                  {'form': form,
                   'course_title': course.title,
                   'editing': editing,
                   'title': page_title})


def update_course_tags(form, course, user):
    tags = form.cleaned_data.get("tags", "").strip().split(",")
    is_draft = form.cleaned_data.get("is_draft")
    course.is_draft = is_draft
    course.save()
    # remove any existing tags
    CourseTag.objects.filter(course=course).delete()
    # now add the new ones
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
