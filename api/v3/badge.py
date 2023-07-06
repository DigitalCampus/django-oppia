from oppia.models import Badge
from rest_framework import serializers, viewsets


class BadgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Badge
        fields = ['id',
                  'allow_multiple_awards',
                  'default_icon',
                  'description',
                  'name',
                  'points',
                  'ref']


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    http_method_names = ['get']
