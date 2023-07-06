from activitylog.models import UploadedActivityLog
from rest_framework import serializers, viewsets


class ActivityLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedActivityLog
        fields = ['created_date']


class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = UploadedActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    http_method_names = ['patch']
