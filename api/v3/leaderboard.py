from oppia.models import Points
from rest_framework import serializers, viewsets


class LeaderboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Points
        fields = ['date',
                  'description',
                  'points',
                  'type']


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Points.objects.all()
    serializer_class = LeaderboardSerializer
    http_method_names = ['get']
