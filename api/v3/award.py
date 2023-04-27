from oppia.models import Award
from rest_framework import serializers, viewsets


class AwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Award
        fields = ['description', 'award_date', 'certificate_pdf']


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    http_method_names = ['get']
