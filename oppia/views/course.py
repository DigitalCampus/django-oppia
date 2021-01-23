import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView, FormView

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
    can_view_courses_list, can_upload
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
        elif course_filter == 'live':
            courses = courses.filter(is_archived=False, is_draft=False)

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


class CanUploadCoursePermission(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return can_upload(self.request.user)


class UploadStep1(CanUploadCoursePermission, FormView):
    form_class = UploadCourseStep1Form
    template_name = 'course/form.html'
    extra_context = { 'title': _(u'Upload Course - step 1')}

    def form_valid(self, form):
        user = self.request.user
        extract_path = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', str(user.id))
        course, resp = handle_uploaded_file(self.request.FILES['course_file'],
                                            extract_path, self.request, user)
        if course:
            CoursePublishingLog(course=course, user=user, action="file_uploaded",
                                data=self.request.FILES['course_file'].name).save()
            return HttpResponseRedirect(reverse('oppia:upload_step2', args=[course.id]))
        else:
            return super().form_invalid(form)


class CanEditCoursePermission(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return can_edit_course(self.request, self.kwargs[self.pk_url_kwarg])


class CourseFormView(CanEditCoursePermission, FormView):
    template_name = 'course/form.html'
    form_class = UploadCourseStep2Form
    pk_url_kwarg = 'course_id'

    def get_success_url(self):
        return reverse('oppia:course')

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(pk=kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'tags': self.course.get_tags(),
                'is_draft': self.course.is_draft, }

    def form_valid(self, form):
        self.update_course_tags(form, self.course, self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_title'] = self.course.title
        return context

    def update_course_tags(self, form, course, user):
        tags = form.cleaned_data.get("tags", "").strip().split(",")
        is_draft = form.cleaned_data.get("is_draft")
        course.is_draft = is_draft
        course.save()
        # remove any existing tags
        CourseTag.objects.filter(course=course).delete()
        # now add the new ones
        for t in tags:
            tag, created = Tag.objects.get_or_create(name=t.strip())
            if created:
                tag.created_by = user
                tag.save()
            # add tag to course
            if not CourseTag.objects.filter(course=course, tag=tag).exists():
                ct = CourseTag()
                ct.course = course
                ct.tag = tag
                ct.save()


class EditCourse(CourseFormView):
    extra_context = {
        'editing': True,
        'title': _(u'Edit course')
    }


class UploadStep2(CanUploadCoursePermission, CourseFormView):
    extra_context = {
        'editing': False,
        'title': _(u'Upload Course - step 2')
    }

    def get_success_url(self):
        return reverse('oppia:upload_success')

    def form_valid(self, form):
        CoursePublishingLog(
            course=self.course,
            new_version=self.course.version,
            user=self.request.user,
            action="upload_course_published",
            data=_(u'Course published via file upload')).save()

        return super().form_valid(form)


class CourseStructure(CanEditCoursePermission, DetailView):
    template_name = 'course/structure.html'
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'
    model = Course


class CourseDataExports(CanEditCoursePermission, DetailView):
    template_name = 'course/export.html'
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'
    model = Course
