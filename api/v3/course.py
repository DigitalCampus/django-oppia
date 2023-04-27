from oppia.models import Course
from rest_framework import serializers, viewsets


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['id',
                  'description',
                  'priority',
                  'restricted',
                  'shortname',
                  'status',
                  'title',
                  'url',
                  'version']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    http_method_names = ['get', 'post']
