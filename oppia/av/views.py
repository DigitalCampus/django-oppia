# oppia/av/views.py
import datetime

from django.conf import settings
from django.core import exceptions
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.av.forms import UploadMediaForm
from oppia.av.models import UploadedMedia, UploadedMediaImage
from oppia.av import handler


def home_view(request):
    uploaded_media = []

    objs = UploadedMedia.objects.all().order_by('-created_date')
    for o in objs:
        embed_code = o.get_embed_code(request.build_absolute_uri(o.file.url))
        uploaded_media.append({'uploaded_media': o, 'embed_code': embed_code})

    paginator = Paginator(uploaded_media, 25)

    try:
        page = int(request.GET. get('page', '1'))
    except ValueError:
        page = 1

    try:
        media = paginator.page(page)
    except (EmptyPage, InvalidPage):
        media = paginator.page(paginator.num_pages)

    return render(request, 'oppia/av/home.html',
                              {'title': _(u'Uploaded Media'),
                                'page': media})


def upload_view(request):
    if not request.user.userprofile.get_can_upload():
        raise exceptions.PermissionDenied

    if request.method == 'POST':
        result = handler.upload(request, request.user)

        if result['result'] == UploadedMedia.UPLOAD_STATUS_SUCCESS:
            return HttpResponseRedirect(reverse('oppia_av_upload_success', args=[result['media'].id]))
        else:
            form = result['form']
    else:
        form = UploadMediaForm()  # An unbound form

    return render(request, 'oppia/av/upload.html',
                              {'form': form,
                               'title': _(u'Upload Media')})


def upload_success_view(request, id):
    if not request.user.userprofile.get_can_upload():
        raise exceptions.PermissionDenied

    media = get_object_or_404(UploadedMedia, pk=id)

    embed_code = media.get_embed_code(request.build_absolute_uri(media.file.url))

    return render(request, 'oppia/av/upload_success.html',
                              {'title': _(u'Upload Media'),
                               'media': media,
                               'embed_code': embed_code})


def media_view(request, id):
    if not request.user.userprofile.get_can_upload():
        raise exceptions.PermissionDenied

    media = get_object_or_404(UploadedMedia, pk=id)

    embed_code = media.get_embed_code(request.build_absolute_uri(media.file.url))

    return render(request, 'oppia/av/view.html',
                              {'title': _(u'Media'),
                               'media': media,
                               'embed_code': embed_code})


def set_default_image_view(request, image_id):
    if not request.user.userprofile.get_can_upload():
        raise exceptions.PermissionDenied

    media = UploadedMedia.objects.get(images__pk=image_id)

    # reset all images to not be default
    images = UploadedMediaImage.objects.filter(uploaded_media=media)
    for i in images:
        i.default_image = False
        i. save()

    # set the selected one
    image = UploadedMediaImage.objects.get(pk=image_id)
    image.default_image = True
    image.save()

    return HttpResponseRedirect(reverse('oppia_av_view', args=[media.id]))
