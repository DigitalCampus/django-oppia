from oppia.models import Points
from rest_framework import serializers, viewsets


class PointsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Points
        fields = ['date',
                  'description',
                  'points',
                  'type']


class PointsViewSet(viewsets.ModelViewSet):
    queryset = Points.objects.all()
    serializer_class = PointsSerializer
    http_method_names = ['get']
