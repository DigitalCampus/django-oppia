import os

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
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
from reports.signals import dashboard_accessed
from summary.models import UserCourseSummary


class CourseListView(ListView, AjaxTemplateResponseMixin):

    template_name = 'course/list.html'
    ajax_template_name = 'course/query.html'
    default_order = 'title'
    paginate_by = 20

    def get_queryset(self):

        courses = can_view_courses_list(self.request, self.get_ordering())
        course_filter = self.get_filter()
        if course_filter == 'draft':
            courses = courses.filter(is_draft=True)
        elif course_filter == 'archived':
            courses = courses.filter(is_archived=True)

        tag = self.get_current_tag()
        if tag is not None:
            courses = courses.filter(coursetag__tag__pk=tag)

        return courses

    def get_current_tag(self):
        return self.kwargs['tag_id'] if 'tag_id' in self.kwargs else None

    def get_ordering(self):
        return self.request.GET.get('order_by', self.default_order)

    def get_filter(self):
        return self.request.GET.get('visibility', '')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_accessed.send(sender=None, request=self.request, data=None)

        course_list = context['page_obj'].object_list
        course_stats = UserCourseSummary.objects\
            .filter(course__in=list(course_list))\
            .aggregated_stats('total_downloads')

        for course in course_list:
            access_detail = can_view_course_detail(self.request, course.id)
            course.can_edit = can_edit_course(self.request, course.id)
            course.access_detail = access_detail is not None
            for stats in course_stats:
                if stats['course'] == course.id:
                    course.distinct_downloads = stats['distinct']
                    course.total_downloads = stats['total']
                    # remove the element to optimize next searches
                    course_stats.remove(stats)

        context['page_ordering'] = self.get_ordering()
        context['tag_list'] = Tag.objects.all() \
            .exclude(coursetag=None) \
            .order_by('name')
        context['current_tag'] = self.get_current_tag()
        context['course_filter'] = self.get_filter()

        return context


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


class CourseStructure(TemplateView):

    def get(self, request, course_id):
        if (not can_edit_course(request, course_id)):
            raise PermissionDenied

        course = Course.objects.get(pk=course_id)

        return render(request, 'course/structure.html',
                      {'course': course})


class CourseDataExports(TemplateView):

    def get(self, request, course_id):
        if (not can_edit_course(request, course_id)):
            raise PermissionDenied

        course = get_object_or_404(Course, pk=course_id)

        return render(request, 'course/export.html',
                      {'course': course})
