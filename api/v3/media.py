from av.models import UploadedMedia
from rest_framework import serializers, viewsets


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedMedia
        fields = ['id',
                  'file',
                  'md5',
                  'length',
                  'title',
                  'organisation',
                  'license']


class MediaViewSet(viewsets.ModelViewSet):
    queryset = UploadedMedia.objects.all()
    serializer_class = MediaSerializer
    http_method_names = ['get', 'post']

    # post - for posting new media

    # get - for retrieving media file
