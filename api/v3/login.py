from django.contrib.auth.models import User
from rest_framework import serializers, viewsets


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email']


class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ['post']

    # post - for logging in
