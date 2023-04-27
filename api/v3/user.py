from django.contrib.auth.models import User
from rest_framework import serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email'
                  ]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
