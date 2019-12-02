from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource

from api.serializers import PrettyJSONSerializer
from oppia.models import Badge


class BadgesResource(ModelResource):
    class Meta:
        queryset = Badge.objects.all()
        allowed_methods = ['get']
        resource_name = 'badges'
        include_resource_uri = False
        serializer = PrettyJSONSerializer()
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['default_icon'] = bundle.request \
            .build_absolute_uri(bundle.data['default_icon'])
        return bundle
