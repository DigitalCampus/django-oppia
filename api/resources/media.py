from django.conf.urls import url
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource

from av.models import UploadedMedia


class MediaResource(ModelResource):

    class Meta:
        queryset = UploadedMedia.objects.all()
        allowed_methods = ['get']
        fields = ['file', 'id', 'length', 'md5']
        resource_name = 'media'
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/md5/(?P<md5>\w[\w/-]*)$"
                % (self._meta.resource_name),
                self.wrap_view('media'), name="api_media"),
        ]

    def media(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        md5 = kwargs.pop('md5', None)
        uploadedmedia = get_object_or_404(UploadedMedia, md5=md5)

        file_url = request.build_absolute_uri(uploadedmedia.file.name) \
            .replace('api/v2/media/md5/', 'media/')
        media_obj = {}
        media_obj['digest'] = uploadedmedia.md5
        media_obj['length'] = uploadedmedia.length
        media_obj['filesize'] = uploadedmedia.get_filesize()
        media_obj['filename'] = uploadedmedia.filename()
        media_obj['download_url'] = file_url

        return JsonResponse(media_obj)
