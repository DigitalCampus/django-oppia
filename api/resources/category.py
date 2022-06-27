import json

from django.db.models import Q
from django.http import HttpResponse, Http404
from django.urls.conf import re_path
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from oppia.models import Course, Category, CoursePermissions

from api.resources.course import CourseResource
from oppia.utils.filters import CourseCategoryFilter, CourseFilter


class CategoryResource(ModelResource):
    count = fields.IntegerField(readonly=True)
    count_new_downloads_enabled = fields.IntegerField(readonly=True)
    course_statuses = fields.DictField(readonly=True)

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'tag'
        allowed_methods = ['get']
        fields = ['id',
                  'name',
                  'description',
                  'highlight',
                  'icon',
                  'order_priority']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True
        include_resource_uri = False

    def get_object_list(self, request):
        if request.user.is_staff:
            return Category.objects.filter(
                Q(courses__isnull=False)
                & CourseCategoryFilter.COURSE_IS_NOT_ARCHIVED) \
                .distinct().order_by(
                '-order_priority', 'name')
        else:
            return Category.objects.filter(
                Q(courses__isnull=False)
                & CourseCategoryFilter.COURSE_IS_NOT_ARCHIVED
                & (CourseCategoryFilter.COURSE_IS_NOT_DRAFT
                   | (CourseCategoryFilter.COURSE_IS_DRAFT & Q(coursecategory__course__user=request.user))
                   | (CourseCategoryFilter.COURSE_IS_DRAFT &
                      Q(coursecategory__course__coursepermissions__user=request.user))
                   )
                ) \
                .distinct().order_by('-order_priority', 'name')

    def prepend_urls(self):
        return [
            re_path(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)%s$"
                    % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('tag_detail'),
                    name="api_tag_detail"),
        ]

    def tag_detail(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        pk = kwargs.pop('pk', None)
        try:
            category = self._meta.queryset.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404()

        if request.user.is_staff:
            courses = Course.objects.filter(category=category).filter(CourseFilter.IS_NOT_ARCHIVED).order_by(
                '-priority', 'title')
        else:
            courses = Course.objects.filter(category=category) \
                .filter(CourseFilter.IS_NOT_ARCHIVED) \
                .filter(
                CourseFilter.IS_NOT_DRAFT |
                (CourseFilter.IS_DRAFT & Q(user=request.user)) |
                (CourseFilter.IS_DRAFT & Q(coursepermissions__user=request.user))
            ) \
                .distinct().order_by('-priority', 'title')

        course_data = []
        cr = CourseResource()
        for c in courses:
            bundle = cr.build_bundle(obj=c, request=request)
            cr.full_dehydrate(bundle)
            course_data.append(bundle.data)

        response = HttpResponse(
            content=json.dumps({'id': pk,
                                'count': courses.count(),
                                'courses': course_data,
                                'name': category.name}),
            content_type="application/json; charset=utf-8")
        return response

    def dehydrate_count(self, bundle):
        tmp = Course.objects.filter(category__id=bundle.obj.id).filter(CourseFilter.IS_NOT_ARCHIVED)
        if bundle.request.user.is_staff:
            count = tmp.count()
        else:
            count = tmp.filter(CourseFilter.IS_NOT_DRAFT
                               | (CourseFilter.IS_DRAFT & Q(user=bundle.request.user))
                               | (CourseFilter.IS_DRAFT & Q(pk__in=CoursePermissions.objects.filter(user=bundle.request.user).values('course')))).count()
        return count

    def dehydrate_icon(self, bundle):
        if bundle.data['icon'] is not None:
            return bundle.request.build_absolute_uri(bundle.data['icon'])
        else:
            return None

    def dehydrate_count_new_downloads_enabled(self, bundle):
        courses = Course.objects.filter(category=bundle.obj).filter(CourseFilter.IS_NOT_ARCHIVED)

        if not bundle.request.user.is_staff:
            courses = courses.filter(CourseFilter.IS_NOT_DRAFT
                                     | Q(pk__in=CoursePermissions.objects.filter(user=bundle.request.user).values('course')))

        return courses.filter(category=bundle.obj).filter(CourseFilter.NEW_DOWNLOADS_ENABLED).count()

    def dehydrate_course_statuses(self, bundle):
        courses = Course.objects.filter(category=bundle.obj).filter(CourseFilter.IS_NOT_ARCHIVED)

        if not bundle.request.user.is_staff:
            courses = courses.filter(CourseFilter.IS_NOT_DRAFT \
                                     | Q(pk__in=CoursePermissions.objects.filter(user=bundle.request.user).values('course')))

        return {course.shortname: course.status for course in courses}

    def alter_list_data_to_serialize(self, request, data):
        if isinstance(data, dict) and 'objects' in data:
            data['tags'] = data['objects']
            del data['objects']
        return data
