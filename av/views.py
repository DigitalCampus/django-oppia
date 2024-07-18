# oppia/av/views.py
import os

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, RedirectView

from av import handler
from av.models import UploadedMedia
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from oppia.models import Media, Course
from oppia.permissions import permission_view_course

STR_UPLOAD_MEDIA = _(u'Upload Media')


class AVHome(ListView, AjaxTemplateResponseMixin):

    template_name = 'av/home.html'
    ajax_template_name = 'av/query.html'
    queryset = UploadedMedia.objects.all().order_by('-created_date')
    extra_context = {'title': STR_UPLOAD_MEDIA}
    paginate_by = 25


class CourseMediaList(ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    template_name = 'course/media/list.html'
    ajax_template_name = 'course/media/query.html'
    paginate_by = 10

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        media = Media.objects.filter(course__id=course_id).order_by('id')
        for m in media:
            m.uploaded = UploadedMedia.objects.filter(md5=m.digest).first()
        return media

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_id'])
        context['uploaded'] = 0
        for media in context['paginator'].object_list:
            context['uploaded'] += 1 if media.uploaded else 0

        if self.request.GET.get('error', None) == 'no_media':
            context['no_media'] = True
        return context


def download_media_file(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    uploaded = get_object_or_404(UploadedMedia, md5=media.digest)
    filepath = uploaded.file.path
    with open(filepath, 'rb') as media_file:
        response = HttpResponse(media_file)
        response['Content-Disposition'] = 'attachment; filename="%s"' % (media.filename)
        response['Content-Length'] = os.path.getsize(filepath)
        return response

class ExternalMediaDownloadView(RedirectView):
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        media_filename = kwargs["filename"]
        # check file exists
        if not os.path.isfile(settings.OPPIA_EXTERNAL_STORAGE_MEDIA_ROOT + media_filename):
            raise Http404
        url = settings.OPPIA_EXTERNAL_STORAGE_MEDIA_URL + media_filename
        return url

@permission_view_course
def download_course_media(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    media = Media.objects.filter(course=course)
    uploaded = UploadedMedia.objects.filter(
        md5__in=media.values_list('digest', flat=True))
    for file in uploaded:
        file.media = media.get(digest=file.md5)

    filename = course.shortname + "_media.zip"
    path = handler.zip_course_media(filename, uploaded)

    if path:
        with open(path, 'rb') as package:
            response = HttpResponse(package.read(), content_type='application/zip')
            response['Content-Length'] = os.path.getsize(path)
            response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
            return response
    else:
        return redirect(reverse('av:course_media', kwargs={'course_id': course.pk})+'?error=no_media')
