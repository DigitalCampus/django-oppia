from django.contrib.auth.models import User
from rest_framework import serializers, viewsets


class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email']


class UserDataViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    http_method_names = ['get']

    # profile data

    # quiz

    # activity

    # badges

    # points

    # feedback
