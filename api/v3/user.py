from django.contrib.auth.models import User
from rest_framework import serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete', 'put']

    # Get - for getting profile

    # post - for registering new user

    # delete - for removing an account

    # put - for updating a profile, password update
