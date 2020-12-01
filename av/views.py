# oppia/av/views.py
import os
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from av import constants
from av import handler
from av.forms import UploadMediaForm
from av.models import UploadedMedia, UploadedMediaImage
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from oppia.models import Media, Course
from oppia.permissions import user_can_upload, can_view_course

from reports.signals import dashboard_accessed

STR_UPLOAD_MEDIA = _(u'Upload Media')


class AVHome(TemplateView):
    def get(self, request):
        uploaded_media = []

        objs = UploadedMedia.objects.all().order_by('-created_date')
        for o in objs:
            embed_code = o.get_embed_code(
                request.build_absolute_uri(o.file.url))
            uploaded_media.append({'uploaded_media': o,
                                   'embed_code': embed_code})

        paginator = Paginator(uploaded_media, 25)

        try:
            page = int(request.GET. get('page', '1'))
        except ValueError:
            page = 1

        try:
            media = paginator.page(page)
        except (EmptyPage, InvalidPage):
            media = paginator.page(paginator.num_pages)
        
        dashboard_accessed.send(sender=None, request=request, data=None)
        
        return render(request, 'av/home.html',
                      {'title': STR_UPLOAD_MEDIA,
                       'page': media})


@method_decorator(user_can_upload, name='dispatch')
class Upload(TemplateView):
    def get(self, request):
        form = UploadMediaForm()

        dashboard_accessed.send(sender=None, request=request, data=None)
        
        return render(request, 'common/upload.html',
                      {'form': form,
                       'title': STR_UPLOAD_MEDIA})

    def post(self, request):
        result = handler.upload(request, request.user)

        if result['result'] == constants.UPLOAD_MEDIA_STATUS_SUCCESS:
            return HttpResponseRedirect(reverse('av:upload_success',
                                                args=[result['media'].id]))
        else:
            form = result['form']

        return render(request, 'common/upload.html',
                      {'form': form,
                       'title': STR_UPLOAD_MEDIA})


@method_decorator(user_can_upload, name='dispatch')
class UploadSuccess(TemplateView):
    def get(self, request, id):
        media = get_object_or_404(UploadedMedia, pk=id)

        embed_code = media.get_embed_code(
            request.build_absolute_uri(media.file.url))

        return render(request, 'av/upload_success.html',
                      {'title': STR_UPLOAD_MEDIA,
                       'media': media,
                       'embed_code': embed_code})


@user_can_upload
def media_view(request, id):
    media = get_object_or_404(UploadedMedia, pk=id)

    embed_code = media.get_embed_code(
        request.build_absolute_uri(media.file.url))

    dashboard_accessed.send(sender=None, request=request, data=None)
    
    return render(request, 'av/view.html',
                  {'title': _(u'Media'),
                   'media': media,
                   'embed_code': embed_code})


@user_can_upload
def set_default_image_view(request, image_id):
    media = UploadedMedia.objects.get(images__pk=image_id)

    # reset all images to not be default
    images = UploadedMediaImage.objects.filter(uploaded_media=media)
    for i in images:
        i.default_image = False
        i.save()

    # set the selected one
    image = UploadedMediaImage.objects.get(pk=image_id)
    image.default_image = True
    image.save()

    return HttpResponseRedirect(reverse('av:view', args=[media.id]))


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

    dashboard_accessed.send(sender=None, request=request, data=None)
    
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
