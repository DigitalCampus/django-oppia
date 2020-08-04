import json

from django.conf.urls import url
from django.db.models import Q
from django.http import HttpResponse, Http404
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from oppia.models import Course, Tag

from api.resources.course import CourseResource


class TagResource(ModelResource):
    count = fields.IntegerField(readonly=True)

    class Meta:
        queryset = Tag.objects.all()
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
            return Tag.objects.filter(
                courses__isnull=False,
                coursetag__course__is_archived=False).distinct().order_by(
                    '-order_priority', 'name')
        else:
            return Tag.objects.filter(
                                      courses__isnull=False,
                                      coursetag__course__is_archived=False) \
                .filter(
                        Q(coursetag__course__is_draft=False) |
                        (Q(coursetag__course__is_draft=True)
                         & Q(coursetag__course__user=request.user))) \
                .distinct().order_by('-order_priority', 'name')

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('tag_detail'),
                name="api_tag_detail"),
        ]

    def tag_detail(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        pk = kwargs.pop('pk', None)
        try:
            tag = self._meta.queryset.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404()

        if request.user.is_staff:
            courses = Course.objects.filter(
                tag=tag,
                is_archived=False).order_by('-priority', 'title')
        else:
            courses = Course.objects.filter(tag=tag,
                                            is_archived=False) \
                        .filter(
                                Q(is_draft=False) |
                                (Q(is_draft=True) & Q(user=request.user))) \
                        .order_by('-priority', 'title')

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
                                'name': tag.name}),
            content_type="application/json; charset=utf-8")
        return response

    def dehydrate_count(self, bundle):
        tmp = Course.objects.filter(tag__id=bundle.obj.id, is_archived=False)
        if bundle.request.user.is_staff:
            count = tmp.count()
        else:
            count = tmp.filter(Q(is_draft=False) |
                               (Q(is_draft=True) &
                                Q(user=bundle.request.user))).count()
        return count

    def dehydrate_icon(self, bundle):
        if bundle.data['icon'] is not None:
            return bundle.request.build_absolute_uri(bundle.data['icon'])
        else:
            return None

    def alter_list_data_to_serialize(self, request, data):
        if isinstance(data, dict) and 'objects' in data:
            data['tags'] = data['objects']
            del data['objects']
        return data
