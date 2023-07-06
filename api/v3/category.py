from oppia.models import Category
from rest_framework import serializers, viewsets


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'description',
                  'highlight',
                  'icon',
                  'name',
                  'order_priority']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']
