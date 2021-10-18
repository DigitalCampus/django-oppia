# oppia/av/views.py
import os

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from av import handler
from av.models import UploadedMedia
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin

from oppia.models import Media, Course
from oppia.permissions import can_view_course

STR_UPLOAD_MEDIA = _(u'Upload Media')


class AVHome(ListView, AjaxTemplateResponseMixin):

    template_name = 'av/home.html'
    ajax_template_name = 'av/query.html'
    queryset = UploadedMedia.objects.all().order_by('-created_date')
    extra_context = {'title': STR_UPLOAD_MEDIA}


class CourseMediaList(ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    template_name = 'course/media/list.html'
    ajax_template_name = 'course/media/query.html'
    paginate_by = 10

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Media.objects.filter(course__id=course_id).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])
        context['uploaded'] = 0
        for media in context['object_list']:
            media.uploaded = UploadedMedia.objects \
                .filter(md5=media.digest).first()
            context['uploaded'] += 1 if media.uploaded else 0

        if self.request.GET.get('error', None) == 'no_media':
            context['no_media'] = True
        return context


def download_course_media(request, course_id):
    course = can_view_course(request, course_id)
    digests = Media.objects.filter(course=course).values_list('digest',
                                                              flat=True)
    media = UploadedMedia.objects.filter(md5__in=digests)

    filename = course.shortname + "_media.zip"
    path = handler.zip_course_media(filename, media)

    if path:
        with open(path, 'rb') as package:
            response = HttpResponse(package.read(),
                                    content_type='application/zip')
            response['Content-Length'] = os.path.getsize(path)
            response['Content-Disposition'] = 'attachment; filename="%s"' \
                % (filename)
            return response
    else:
        return redirect(reverse('av:course_media',
                                kwargs={'course_id':
                                        course.pk})+'?error=no_media')
