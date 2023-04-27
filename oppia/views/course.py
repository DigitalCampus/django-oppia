import os

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView, FormView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from oppia.forms.edit import EditCourseForm
from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from oppia.forms.upload import UploadCourseStep1Form, UploadCourseStep2Form
from oppia.models import Category, CourseCategory, CoursePublishingLog, Course
from oppia.permissions import can_edit_course, can_download_course, can_view_courses_list, \
    can_upload, can_edit_course_gamification
from oppia.uploader import handle_uploaded_file
from oppia.utils.filters import CourseFilter
from summary.models import UserCourseSummary


class CourseListView(SafePaginatorMixin, ListView, AjaxTemplateResponseMixin):

    template_name = 'course/list.html'
    ajax_template_name = 'course/query.html'
    default_order = 'title'
    paginate_by = 20

    def get_queryset(self):

        courses = can_view_courses_list(self.request, self.get_ordering())
        course_filter = self.get_filter()
        if course_filter == 'draft':
            courses = courses.filter(CourseFilter.IS_DRAFT)
        elif course_filter == 'archived':
            courses = courses.filter(CourseFilter.IS_ARCHIVED)
        elif course_filter == 'live':
            courses = courses.filter(CourseFilter.IS_LIVE)
        elif course_filter == 'new_downloads_disabled':
            courses = courses.filter(CourseFilter.NEW_DOWNLOADS_DISABLED)
        elif course_filter == 'read_only':
            courses = courses.filter(CourseFilter.IS_READ_ONLY)

        category = self.get_current_category()
        if category is not None:
            courses = courses.filter(coursecategory__category__pk=category)

        return courses

    def get_current_category(self):
        return self.kwargs['category_id'] if 'category_id' in self.kwargs else None

    def get_ordering(self):
        return self.request.GET.get('order_by', self.default_order)

    def get_filter(self):
        return self.request.GET.get('status', '')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course_list = context['page_obj'].object_list
        course_stats = UserCourseSummary.objects\
            .filter(course__in=list(course_list))\
            .aggregated_stats('total_downloads')

        for course in course_list:
            course.access_detail = course.user_can_view_detail(self.request.user)
            course.can_edit = can_edit_course(self.request, course.id)
            course.can_edit_gamification = can_edit_course_gamification(self.request, course.id)
            for stats in course_stats:
                if stats['course'] == course.id:
                    course.distinct_downloads = stats['distinct']
                    course.total_downloads = stats['total']
                    # remove the element to optimize next searches
                    course_stats.remove(stats)

        context['page_ordering'] = self.get_ordering()
        context['category_list'] = Category.objects.all().exclude(coursecategory=None).order_by('name')
        context['current_category'] = self.get_current_category()
        context['course_filter'] = self.get_filter()

        return context


class ManageCourseList(CourseListView):
    template_name = 'course/list_page.html'
    ajax_template_name = 'course/list_page.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ajax_url'] = reverse_lazy('oppia:course_manage')
        return context


class CourseDownload(TemplateView):

    def get(self, request, course_id):
        course = can_download_course(request, course_id)
        file_to_download = course.getAbsPath()
        binary_file = open(file_to_download, 'rb')
        response = HttpResponse(binary_file.read(), content_type='application/zip')
        binary_file.close()
        response['Content-Length'] = os.path.getsize(file_to_download)
        response['Content-Disposition'] = 'attachment; filename="%s"' % (course.filename)

        return response


class CanUploadCoursePermission(UserPassesTestMixin):
    def test_func(self):
        return can_upload(self.request.user)


class UploadStep1(CanUploadCoursePermission, FormView):
    form_class = UploadCourseStep1Form
    template_name = 'course/form.html'
    extra_context = {'title': _(u'Upload Course - step 1')}

    def form_valid(self, form):
        user = self.request.user
        extract_path = os.path.join(settings.COURSE_UPLOAD_DIR, 'temp', str(user.id))
        course, resp, is_new_course = handle_uploaded_file(self.request.FILES['course_file'],
                                                           extract_path,
                                                           self.request,
                                                           user)
        if course:
            CoursePublishingLog(course=course,
                                user=user,
                                action="file_uploaded",
                                data=self.request.FILES['course_file'].name) \
                                .save()
            return HttpResponseRedirect(reverse('oppia:upload_step2', args=[course.id]))
        else:
            return super().form_invalid(form)


class CanEditCoursePermission(UserPassesTestMixin):
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
        return {'categories': self.course.get_categories(),
                'status': self.course.status,
                'restricted': self.course.restricted}

    def form_valid(self, form):
        self.update_course(form, self.course, self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_title'] = self.course.title
        return context

    def update_course(self, form, course, user):
        categories = form.cleaned_data.get('categories', '').strip().split(',')
        if self.extra_context is not None and self.extra_context.get('editing', False):
            course.status = form.cleaned_data.get('status')
        course.restricted = form.cleaned_data.get('restricted')
        course.save()
        # remove any existing tags
        CourseCategory.objects.filter(course=course).delete()
        # now add the new ones
        for c in categories:
            category, created = Category.objects.get_or_create(name=c.strip())
            if created:
                category.created_by = user
                category.save()
            # add tag to course
            if not CourseCategory.objects.filter(course=course, category=category).exists():
                cc = CourseCategory()
                cc.course = course
                cc.category = category
                cc.save()


class EditCourse(CourseFormView):
    form_class = EditCourseForm
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
