import json
import os
import shutil
import zipfile

from django.conf import settings
from django.conf.urls import url
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from api.serializers import CourseJSONSerializer
from oppia.models import Tracker, Course, CourseTag
from oppia.signals import course_downloaded


class CourseResource(ModelResource):

    STR_COURSE_NOT_FOUND = _(u"Course not found")

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        allowed_methods = ['get']
        fields = ['id',
                  'title',
                  'version',
                  'shortname',
                  'priority',
                  'is_draft',
                  'description',
                  'author',
                  'username',
                  'organisation']
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        serializer = CourseJSONSerializer()
        always_return_data = True
        include_resource_uri = True

    def get_object_list(self, request):
        if request.user.is_staff:
            return Course.objects.filter(is_archived=False) \
                .order_by('-priority', 'title')
        else:
            return Course.objects.filter(is_archived=False) \
                .filter(
                        Q(is_draft=False) |
                        (Q(is_draft=True) & Q(user=request.user))) \
                .order_by('-priority', 'title')

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/download%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('download_course'), name="api_download_course"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/activity%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('download_activity'),
                name="api_download_activity"),
        ]

    def get_course(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        pk = kwargs.pop('pk', None)
        try:
            if request.user.is_staff:
                course = self._meta.queryset.get(pk=pk, is_archived=False)
            else:
                course = self._meta.queryset \
                    .filter(
                            Q(is_draft=False) |
                            (Q(is_draft=True) & Q(user=request.user))) \
                    .get(pk=pk, is_archived=False)
        except Course.DoesNotExist:
            raise Http404(self.STR_COURSE_NOT_FOUND)
        except ValueError:
            try:
                if request.user.is_staff:
                    course = self._meta.queryset.get(shortname=pk,
                                                     is_archived=False)
                else:
                    course = self._meta.queryset \
                        .filter(
                                Q(is_draft=False) |
                                (Q(is_draft=True) & Q(user=request.user))) \
                        .get(shortname=pk, is_archived=False)
            except Course.DoesNotExist:
                raise Http404(self.STR_COURSE_NOT_FOUND)

        return course

    def download_course(self, request, **kwargs):
        course = self.get_course(request, **kwargs)

        file_to_download = course.getAbsPath()
        has_completed_trackers = Tracker.has_completed_trackers(course,
                                                                request.user)

        try:
            if has_completed_trackers:
                file_to_download = os.path.join(
                    settings.COURSE_UPLOAD_DIR,
                    "temp",
                    str(request.user.id) + "-" + course.filename)
                shutil.copy2(course.getAbsPath(), file_to_download)
                course_zip = zipfile.ZipFile(file_to_download, 'a')
                if has_completed_trackers:
                    course_zip.writestr(course.shortname + "/tracker.xml",
                                        Tracker.to_xml_string(course,
                                                              request.user))
                course_zip.close()

            binary_file = open(file_to_download, 'rb')
            response = HttpResponse(binary_file.read(),
                                    content_type='application/zip')
            binary_file.close()
            response['Content-Length'] = os.path.getsize(file_to_download)
            response['Content-Disposition'] = \
                'attachment; filename="%s"' % (course.filename)
        except IOError:
            raise Http404(self.STR_COURSE_NOT_FOUND)

        course_downloaded.send(sender=self, course=course, request=request)

        return response

    def download_activity(self, request, **kwargs):
        course = self.get_course(request, **kwargs)

        return HttpResponse(Tracker.to_xml_string(course,
                                                  request.user),
                            content_type='text/xml')

    def dehydrate(self, bundle):
        bundle.data['url'] = bundle.request.build_absolute_uri(
            bundle.data['resource_uri'] + 'download/')

        # make sure title is shown as json object (not string representation \
        # of one)
        bundle.data['title'] = json.loads(bundle.data['title'])

        try:
            bundle.data['description'] = json.loads(bundle.data['description'])
        except json.JSONDecodeError:
            pass

        course = Course.objects.get(pk=bundle.obj.pk)

        if course and course.user:
            bundle.data['author'] = course.user.first_name \
                                    + " " \
                                    + course.user.last_name
            bundle.data['username'] = course.user.username
            bundle.data['organisation'] = course.user.userprofile.organisation

        return bundle


class CourseTagResource(ModelResource):
    course = fields.ToOneField('api.resource.course.CourseResource',
                               'course',
                               full=True)

    class Meta:
        queryset = CourseTag.objects.all()
        allowed_methods = ['get']
        resource_name = 'coursetag'
        fields = ['id', 'course', 'tag']
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True
